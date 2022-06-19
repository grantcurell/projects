__author__ = "Grant Curell"
__copyright__ = "Do what you want with it"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Grant Curell"

"""
An OpenFlow 1.3 TrafficShaper implementation
"""

import json
import sys
import communityid
import hashlib
import logging
import copy
import urllib3

from webob import Response, Request
from ryu.ofproto.ofproto_v1_3_parser import ofproto_parser, OFPMatch, OFPActionOutput
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller import dpset
from ryu.controller.controller import Datapath
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ipv4, tcp, udp, icmp
from ryu.app.wsgi import WSGIApplication, route
from ryu.app.ofctl_rest import StatsController, RestStatsApi
from ryu.cmd import manager
from collections import defaultdict
from pprint import pformat
from typing import List

gelante_instance_name = 'gelante_app'
supported_protocols = ["tcp", "udp", "icmp"]
angular_port = 4200


def remove_all_flows(datapath: Datapath):
    """
    Removes all the flows from a switch.

    :param datapath: A Datapath object which represents the switch from which we want to remove flows
    """

    match = datapath.ofproto_parser.OFPMatch()
    mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, datapath.ofproto.OFPTT_ALL,
                                             datapath.ofproto.OFPFC_DELETE,
                                             0, 0, 0, 0xffffffff,
                                             datapath.ofproto.OFPP_ANY,
                                             datapath.ofproto.OFPG_ANY,
                                             0, match, [])

    datapath.send_msg(mod)


def delete_flow(datapath: Datapath, match: OFPMatch, out_port: int = None, out_group: int = None):
    """
    Deletes a specified flow from a switch.

    :param datapath: The datapath of the switch from which you want to delete a flow.
    :param match: An OFPMatch object representing the criteria of the flow you want to delete.
    :param out_port: Allows you to specify that you want to delete a flow with a specific output port.
                     If not specified, the default is any port.
    :param out_group:  Allows you to specify that you want to delete a flow with a specific output group.
                       If not specified, the default is any group.
    """

    if out_port is None:
        out_port = datapath.ofproto.OFPP_ANY

    if out_group is None:
        out_group = datapath.ofproto.OFPG_ANY

    try:
        mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, datapath.ofproto.OFPTT_ALL,
                                                 datapath.ofproto.OFPFC_DELETE,
                                                 0, 0, 0, 0xffffffff,
                                                 out_port,
                                                 out_group,
                                                 0, match, [])
    except AssertionError as e:
        print("Unexpected error:", e)
        raise

    datapath.send_msg(mod)


def add_flow(datapath: Datapath, priority: int, match: OFPMatch, actions: [OFPActionOutput], idle_timeout: int = 300,
             hard_timeout: int = 300):
    """
    Send a flow to the switch to be added to the flow table

    :param datapath: A Datapath object which represents the switch to which we want to add the flow
    :param priority: The priority of the flow. Should be higher than zero. Zero is the default flow used when traffic
                     does not match and should be sent to the controller.
    :param match: An OFPMatch object containing the match criteria for this flow
    :param actions: The actions you want applied if there is a flow match.
    :param idle_timeout: The timeout for the flow if the switch receives no matching packets. 0 is no timeout.
    :param hard_timeout: The timeout for the flow regardless if the switch does or doesn't receive packets.
                         0 is no timeout.
    """

    ofproto = datapath.ofproto

    # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
    # module. ryu.ofproto.ofproto_v1_3_parser
    parser = datapath.ofproto_parser

    # construct flow_mod message and send it.
    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                         actions)]

    # The class corresponding to the Flow Mod message is the OFPFlowMod class. The instance of the OFPFlowMod
    # class is generated and the message is sent to the OpenFlow switch using the Datapath.send_msg() method.
    mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst,
                            idle_timeout=idle_timeout, hard_timeout=hard_timeout)
    datapath.send_msg(mod)


def get_packet_type(pkt: packet.Packet) -> dict:
    """
    Returns a dictionary containing a packet's type and the corresponding layers of any supported protocols. See the
    readme for a list of supported protocols.

    :param pkt: The packet whose data we want to evaluate
    :return: A dictionary containing the packet's metadata. The packet's type will be stored under the "type" key.
    """

    pkt_metadata = {}
    pkt_metadata["type"] = "unsupported"

    for index, protocol in enumerate(pkt.protocols, start=0):
        if type(protocol) == ipv4.ipv4:
            pkt_metadata["ipv4"] = index
            pkt_metadata["ipv4_src"] = protocol.src
            pkt_metadata["ipv4_dst"] = protocol.dst
        elif type(protocol) == tcp.tcp:
            pkt_metadata["type"] = "tcp"
            pkt_metadata["tcp"] = index
            pkt_metadata["transport_layer"] = index  # Works for both TCP and UDP
            pkt_metadata["src_port"] = protocol.src_port
            pkt_metadata["dst_port"] = protocol.dst_port
        elif type(protocol) == udp.udp:
            pkt_metadata["type"] = "udp"
            pkt_metadata["udp"] = index
            pkt_metadata["transport_layer"] = index  # Works for both TCP and UDP
            pkt_metadata["src_port"] = protocol.src_port
            pkt_metadata["dst_port"] = protocol.dst_port
        elif type(protocol) == icmp.icmp:
            pkt_metadata["type"] = "icmp"
            pkt_metadata["icmp"] = index
            pkt_metadata["icmp_type"] = protocol.type
            pkt_metadata["icmp_code"] = protocol.code

    return pkt_metadata


def get_tcp_udp_flows(port_type: str, outport: int, dpid: int, priority: int=1) -> [dict]:
    """
    A utility function used to find all of the tcp and udp related flows associated with a specific outport.

    :param port_type: This can "TCP", "UDP", or "ANY" - TODO: Currently only ANY is implemented
    :param outport: The outport for which you want to find flows.
    :param dpid: The DPID for the switch from which you want to retrieve data
    :param priority: Used to specify the priority you want to match against. Typically used for redirect ports.
    :return: Returns an array of dictionaries containing each flow's information
    """

    http = urllib3.PoolManager()

    flow_data = http.request('GET', 'http://127.0.0.1:8080/stats/flow/' + str(dpid))

    try:
        flow_data = json.loads(flow_data.data.decode('utf-8'))
    except:
        logging.error("Unexpected error while retrieving data from backend API. The request we made was for "
                      "\'http://127.0.0.1:8080/stats/flow/\'" + str(dpid) + " We received error "
                      + sys.exc_info()[0])
        raise

    # Used to keep track of all the flows that match TCP or UDP flows
    flow_matches = []  # type: []

    # TODO - need to handle the controller's interface!!!

    for flow in flow_data[str(dpid)]:

        if ("tp_src" in flow["match"] or "tp_dst" in flow["match"]) and flow["actions"][0] == "OUTPUT:" + str(outport) and flow["priority"] == priority:
            flow_matches.append(flow)

    return flow_matches


def get_flow_hash(pkt_metadata: dict) -> str:
    """
    Gets the hash of a given flow. Returns None if the protocol is not supported. See the readme for a list of supported
    protocols.

    :param pkt_metadata: A dictionary containing all packet metadata. Can be retrieved with get_packet_type.
    :return: A string in the form of '1:D0Hb5PnRilB52ktTszXCb9PSY8M=' containing the hash.
    """

    cid = communityid.CommunityID()

    if pkt_metadata["type"] == "tcp":
        tpl = communityid.FlowTuple.make_tcp(
            pkt_metadata["ipv4_src"],
            pkt_metadata["ipv4_dst"],
            pkt_metadata["src_port"],
            pkt_metadata["dst_port"])
        flow_hash = cid.calc(tpl)
    elif pkt_metadata["type"] == "udp":
        tpl = communityid.FlowTuple.make_udp(
            pkt_metadata["ipv4_src"],
            pkt_metadata["ipv4_dst"],
            pkt_metadata["src_port"],
            pkt_metadata["dst_port"])
        flow_hash = cid.calc(tpl)
    elif pkt_metadata["type"] == "icmp":
        tpl = hashlib.sha256()
        tpl.update((pkt_metadata["ipv4_src"] + " " + pkt_metadata["ipv4_dst"]).encode())
        flow_hash = tpl.digest()
    else:
        flow_hash = None

    return flow_hash


def create_flow_match_rules(pkt_metadata: dict, in_port: int, parser: ofproto_parser) -> tuple:
    """
    Creates the bidirectional flow match rules for a given packet.

    :param pkt_metadata: A dictionary containing all packet metadata. Can be retrieved with get_packet_type.
    :param in_port: Switch in_port
    :param parser: A parser for the specific version of OpenFlow you are using
    :return: A tuple containing the inbound flow match rules and the opposite set to account for both directions
    """

    if pkt_metadata["type"] == "tcp":
        match_in = parser.OFPMatch(
            in_port=in_port,
            eth_type=int("800", 16),  # This is a prerequisite for matching against IPv4 packets
            ip_proto=6,  # This is a prerequisite for matching against TCP segments
            ipv4_src=pkt_metadata["ipv4_src"],
            ipv4_dst=pkt_metadata["ipv4_dst"],
            tcp_src=pkt_metadata["src_port"],
            tcp_dst=pkt_metadata["dst_port"])
        match_out = parser.OFPMatch(
            in_port=in_port,
            eth_type=int("800", 16),
            ip_proto=6,  # This is TCP
            ipv4_dst=pkt_metadata["ipv4_src"],
            ipv4_src=pkt_metadata["ipv4_dst"],
            tcp_dst=pkt_metadata["src_port"],
            tcp_src=pkt_metadata["dst_port"])
    elif pkt_metadata["type"] == "udp":
        match_in = parser.OFPMatch(
            in_port=in_port,
            eth_type=int("800", 16),
            ip_proto=17,  # This is UDP
            ipv4_src=pkt_metadata["ipv4_src"],
            ipv4_dst=pkt_metadata["ipv4_dst"],
            udp_src=pkt_metadata["src_port"],
            udp_dst=pkt_metadata["dst_port"])
        match_out = parser.OFPMatch(
            in_port=in_port,
            eth_type=int("800", 16),
            ip_proto= 17,  # This is UDP
            ipv4_dst=pkt_metadata["ipv4_src"],
            ipv4_src=pkt_metadata["ipv4_dst"],
            udp_dst=pkt_metadata["src_port"],
            udp_src=pkt_metadata["dst_port"])
    elif pkt_metadata["type"] == "icmp":
        match_in = parser.OFPMatch(
            eth_type=int("800", 16),
            ip_proto=1,  # This is ICMP
            ipv4_src=pkt_metadata["ipv4_src"],
            ipv4_dst=pkt_metadata["ipv4_dst"])
        match_out = parser.OFPMatch(
            eth_type=int("800", 16),
            ip_proto=1,  # This is ICMP
            ipv4_dst=pkt_metadata["ipv4_src"],
            ipv4_src=pkt_metadata["ipv4_dst"])
    else:
        return ()

    return match_in, match_out


def create_response(req: Request, body: str = None, content_type: str = "application/json") -> Response:
    """
    Responds to Cross-origin resource sharing (CORS) requests. Only permits responses to localhost.

    :param body: The body of the request object that has been sent
    :param content_type: The content type of the response
    :param req: The inbound HTTP request in which we want to check for a CORS header
    :return: Returns a list of headers including a valid CORS response if the request came from the localhost and the
             HTTP origin was specified otherwise returns an empty list.

    """

    environ = req.headers.environ

    method = environ.get("REQUEST_METHOD")
    origin = environ.get("HTTP_ORIGIN")
    cookie = environ.get("HTTP_COOKIE", "N/A")
    logging.info("")
    logging.info("Method: " + method + " Path: " + environ["PATH_INFO"])
    if origin:
        logging.info("Origin: " + origin)
    if cookie:
        logging.info("Cookie: " + cookie)

    cors = origin
    preflight = cors and method == "OPTIONS"

    headers = [("Content-Type", content_type)]

    if cors and ("http://localhost:" + str(angular_port) == cors or "http://127.0.0.1:" + str(angular_port) == cors):
        headers.extend([
            ("Access-Control-Allow-Origin", origin),
            ("Access-Control-Allow-Credentials", "true")
        ])
        if preflight:
            headers.extend([
                ("Access-Control-Allow-Methods", "PUT, GET"),
                ("Access-Control-Allow-Headers", "Content-Type")
            ])
    else:
        headers.append(("Set-Cookie", "auth=fnd"))

    if method == "OPTIONS":
        return Response(status=204, headerlist=headers)
    else:
        return Response(content_type=content_type, text=body, headerlist=headers, status=200)


class GelanteShape:
    """
    This is the main Ryu app that is the Ryu controller

    In order to implement as a Ryu application, ryu.base.app_manager.RyuApp is inherited. Also, to use OpenFlow 1.3, the
    OpenFlow 1.3 version is specified for OFP_VERSIONS.

    Attributes:
        mac_to_port (dict): Used to store information mapping MAC addresses to a specific port
        flow_table (dict): Used to store flow information mapped to a specific port. If the controller receives a packet
                           not already associated with a flow, it creates a flow entry and then maps it to an outbound
                           port
        round_robin (int): Used to keep track of the next port a flow should be assigned to. We use this to load balance
                           flows across multiple ports.
        switches (dict): A dictionary of form {dpid: Datapath} with all of the devices being managed by this controller
        in_ports (defaultdict): Used to keep track of all ports expected to be used for inbound traffic.
        out_ports (defaultdict): Used to keep track of all the ports used for outbound traffic

    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(GelanteShape, self).__init__(*args, **kwargs)
        # mac_to_port is the MAC address table for the switch
        self.mac_to_port = {}
        self.flow_table = {}
        self.round_robin = 0
        self.switches = {}
        self.in_ports = defaultdict(list)
        self.out_ports = defaultdict(list)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        See https://osrg.github.io/ryu-book/en/html/switching_hub.html#event-handler for description.
        See https://osrg.github.io/ryu-book/en/html/switching_hub.html#adding-table-miss-flow-entry for the rest of the
        function details.

        This function handles the ryu.controller.handler.CONFIG_DISPATCHER state. This state is used to handle waiting
        to receive SwitchFeatures message.

        :param ev: The switch event object containing the message data For this function we expect an instance of
                   ryu.ofproto.ofproto_v1_3_parser.OFPSwitchFeatures
        :return:
        """

        # In datapath we expect the instance of the ryu.controller.controller.Datapath class corresponding to the
        # OpenFlow switch that issued this message is stored. The Datapath class performs important processing such as
        # actual communication with the OpenFlow switch and issuance of the event corresponding to the received message.
        datapath = ev.msg.datapath

        # Indicates the ofproto module that supports the OpenFlow version in use. In the case of OpenFlow 1.3 format
        # will be following module. ryu.ofproto.ofproto_v1_3
        ofproto = datapath.ofproto

        # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
        # module. ryu.ofproto.ofproto_v1_3_parser
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        # The Table-miss flow entry has the lowest (0) priority and this entry matches all packets. In the instruction
        # of this entry, by specifying the output action to output to the controller port, in case the received packet
        # does not match any of the normal flow entries, Packet-In is issued.
        #
        # An empty match is generated to match all packets. Match is expressed in the OFPMatch class.
        #
        # Next, an instance of the OUTPUT action class (OFPActionOutput) is generated to transfer to the controller
        # port. The controller is specified as the output destination and OFPCML_NO_BUFFER is specified to max_len in
        # order to send all packets to the controller.
        match = parser.OFPMatch()

        actions: List[OFPActionOutput] = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]

        # Clear out all existing flows on the switch before continuing
        # remove_all_flows(datapath) # TODO - may want this for testing

        # Finally, 0 (lowest) is specified for priority and the add_flow() method is executed to send the Flow Mod
        # message. The content of the add_flow() method is explained in a later section.
        add_flow(datapath, 0, match, actions, 0, 0)

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto

        if msg.reason == ofp.OFPRR_IDLE_TIMEOUT:
            reason = 'IDLE TIMEOUT'
        elif msg.reason == ofp.OFPRR_HARD_TIMEOUT:
            reason = 'HARD TIMEOUT'
        elif msg.reason == ofp.OFPRR_DELETE:
            reason = 'DELETE'
        elif msg.reason == ofp.OFPRR_GROUP_DELETE:
            reason = 'GROUP DELETE'
        else:
            reason = 'unknown'

        self.logger.debug('OFPFlowRemoved received: '
                          'cookie=%d priority=%d reason=%s table_id=%d '
                          'duration_sec=%d duration_nsec=%d '
                          'idle_timeout=%d hard_timeout=%d '
                          'packet_count=%d byte_count=%d match.fields=%s',
                          msg.cookie, msg.priority, reason, msg.table_id,
                          msg.duration_sec, msg.duration_nsec,
                          msg.idle_timeout, msg.hard_timeout,
                          msg.packet_count, msg.byte_count, msg.match)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """
        See https://osrg.github.io/ryu-book/en/html/switching_hub.html#event-handler for description.

        This function handles the ryu.controller.handler.MAIN_DISPATCHER state. This state is used to handle a new
        inbound packet

        :param ev: The event containing the packet data.
        """

        msg = ev.msg
        datapath = msg.datapath

        # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
        # module. ryu.ofproto.ofproto_v1_3_parser
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id  # 64-bit OpenFlow Datapath ID of the switch to which the port belongs.

        # Get the OpenFlow protocol in use.
        ofproto = datapath.ofproto

        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        pkt_metadata = get_packet_type(pkt)

        if in_port in self.in_ports.get(dpid, []) and pkt_metadata["type"] != "unsupported" \
                and len(self.out_ports.get(dpid, [])) > 0:

            flow_hash = get_flow_hash(pkt_metadata)

            # TODO - need a time out for the local hash table. Must match timeout on the switch.
            if flow_hash in self.flow_table:

                out_port = self.flow_table[flow_hash]

                # self.logger.debug("Received an existing flow: %s", pformat(pkt.protocols)) TODO RE-ENABLE THIS

                # construct action list.
                actions = [parser.OFPActionOutput(out_port)]

                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data

                out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=in_port,
                                          actions=actions,
                                          data=data)

                datapath.send_msg(out)

            else:
                self.flow_table[flow_hash] = self.out_ports[dpid][self.round_robin]
                out_port = self.out_ports[dpid][self.round_robin]

                # The flow calculation only works unidirectionally on icmp so we have to enter two different hashes
                # for it.
                # TODO - There is still some strange behavior surrounding ping. Sometimes it's still coming to the controller
                # TODO - or arriving out of order when it's net expected.
                if pkt_metadata["type"] == "icmp":
                    tmp_metadata = copy.deepcopy(pkt_metadata)
                    tmp_metadata["ipv4_src"] = pkt_metadata["ipv4_dst"]
                    tmp_metadata["ipv4_dst"] = pkt_metadata["ipv4_src"]
                    self.flow_table[get_flow_hash(tmp_metadata)] = self.out_ports[dpid][self.round_robin]

                self.round_robin = self.round_robin + 1
                if self.round_robin >= len(self.out_ports[dpid]):
                    self.round_robin = 0

                # self.logger.debug("Received new flow: %s", pformat(pkt.protocols)) TODO - RE-ENABLE THIS

                # construct action list.
                actions = [parser.OFPActionOutput(out_port)]

                match_in, match_out = create_flow_match_rules(pkt_metadata, in_port, parser)

                if match_in and match_out:

                    # For the flow entry this time, the priority is specified to 1. The greater the value, the higher
                    # the priority, therefore, the flow entry added here will be evaluated before the Table-miss flow
                    # entry.
                    add_flow(datapath, 2, match_in, actions)
                    add_flow(datapath, 2, match_out, actions)

                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data

                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=in_port,
                                              actions=actions,
                                              data=data)

                    datapath.send_msg(out)

        else:
            if in_port not in self.in_ports.get(dpid, []):
                self.logger.warning("Received a packet, but we are dropping it because it came in on a port that is not "
                                 "currently set as an input port.")
            elif pkt_metadata["type"] == "unsupported":
                self.logger.warning("Received a packet, but it uses a protocol we do not support. See the readme for "
                                 "supported protocols.")
                self.logger.warning("Packet was: %s", pformat(pkt.protocols))
            elif len(self.out_ports.get(dpid, [])) <= 0:
                self.logger.warning("Received a packet, but there are currently no valid output ports set.")
            else:
                self.logger.warning("Received a packet, but we are dropping it without taking further action. "
                                    "The program was unable to automatically determine the cause for the drop.")
                self.logger.warning("Packet was: %s", pformat(pkt.protocols))


class GelanteShapeRest(GelanteShape, RestStatsApi):
    """
    Overview is here: https://osrg.github.io/ryu-book/en/html/rest_api.html

    This class extends the GelanteShape class above in order to add a REST API functionality.

    """

    # A dictionary to specify contexts which this Ryu application wants to use. Its key is a name of context and its
    # value is an ordinary class which implements the context. The class is instantiated by app_manager and the instance
    # is shared among RyuApp subclasses which has _CONTEXTS member with the same key. A RyuApp subclass can obtain a
    # reference to the instance via its __init__'s kwargs as the following.
    # Class variable _CONTEXT is used to specify Ryu’s WSGI-compatible Web server class. By doing so, WSGI’s Web server
    # instance can be acquired by a key called the wsgi key.
    _CONTEXTS = {
        'wsgi': WSGIApplication,
        'dpset': dpset.DPSet
    }

    def __init__(self, *args, **kwargs):
        self.switches = {}
        wsgi = kwargs['wsgi']

        # For registration, the register method is used. When executing the register method, the dictionary object is
        # passed in the key name gelante_app so that the constructor of the controller can access the instance
        # of the GelanteShapeRest class.
        wsgi.register(GelanteController, {gelante_instance_name: self})
        GelanteShape.__init__(self, *args, **kwargs)
        RestStatsApi.__init__(self, *args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Parent class switch_features_handler is overridden. This method, upon rising of the SwitchFeatures event,
        acquires the datapath object stored in event object ev and stores it in instance variable switches. Also, at
        this time, an empty dictionary is set as the initial value in the MAC address table.

        :param ev: The switch event object containing the message data For this function we expect an instance of
                   ryu.ofproto.ofproto_v1_3_parser.OFPSwitchFeatures
        :return:
        """

        super(GelanteShapeRest, self).switch_features_handler(ev)  # Call the original switch features method
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        self.mac_to_port.setdefault(datapath.id, {})

    def set_mac_to_port(self, dpid: int, entry: json) -> dict:
        """
        Registers a pair of MAC address and port number in the MAC address table and adds a flow entry to the switch.
        The method is executed when REST API is called by the PUT method.

        :param dpid: 64-bit OpenFlow Datapath ID of the switch to which the port belongs.
        :param entry: A JSON entry including the MAC address and port pair you want to store
        :return: A dictionary containing the MAC mappings
        """

        mac_table = self.mac_to_port.setdefault(dpid, {})
        datapath = self.switches.get(dpid)

        entry_port = entry['port']
        entry_mac = entry['mac']

        if datapath is not None:

            # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
            # module. ryu.ofproto.ofproto_v1_3_parser
            parser = datapath.ofproto_parser

            # See https://osrg.github.io/ryu-book/en/html/rest_api.html#implementing-simpleswitchrest13-class for a
            # description of the below.
            if entry_port not in mac_table.values():

                for mac, port in mac_table.items():
                    # from known device to new device
                    actions = [parser.OFPActionOutput(entry_port)]
                    match = parser.OFPMatch(in_port=port, eth_dst=entry_mac)
                    add_flow(datapath, 1, match, actions)

                    # from new device to known device
                    actions = [parser.OFPActionOutput(port)]
                    match = parser.OFPMatch(in_port=entry_port, eth_dst=mac)
                    add_flow(datapath, 1, match, actions)

                mac_table.update({entry_mac: entry_port})

        return mac_table

    def get_datapath(self, dpid: int) -> Datapath:
        """
        Allows you to retrieve the Datapath for a switch with the associated DPID

        :param dpid: The dpid you want to retrieve.
        :return: a Datapath object representing the given switch or None if it is not found.
        """

        return self.switches.get(dpid, None)


class GelanteController(StatsController):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
        'dpset': dpset.DPSet
    }

    def __init__(self, req, link, data, **config):
        data["dpset"] = data[gelante_instance_name].dpset

        # waiters in this case is ultimately used by ofctl_utils.py. It appears to be used for locks
        data["waiters"] = {}
        super(GelanteController, self).__init__(req, link, data, **config)
        self.gelante_app = data[gelante_instance_name]

    @route('/gelante', '/gelante/mactable/{dpid}', methods=['GET'])
    def list_mac_table(self, req, **kwargs) -> Response:
        """
        Retrieves and returns the MAC address table of the specified switch. The REST API is called by the URL
        specified by the second argument. If the HTTP method at that time is GET, the list_mac_table method is called.
        This method acquires the MAC address table corresponding to the data path ID specified in the {dpid} part,
        converts it to the JSON format and returns it to the caller. If the data path ID of an unknown switch, which is
         not connected to Ryu, is specified, response code 404 is returned.
        
        :param req: Used to generate the appropriate CORs headers, but otherwise unused in this function.
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch from which you want to dump
                       the MAC address table
        :return: Returns JSON containing the MAC address table of the specified switch.
        """

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])

        if dpid not in switch_instance.mac_to_port:
            return Response(status=404)

        mac_table = switch_instance.mac_to_port.get(dpid, {})
        body = json.dumps(mac_table)
        return Response(content_type='application/json', text=body)

    @route('/gelante', '/gelante/mactable/{dpid}', methods=['PUT'])
    def put_mac_table(self, req: json, **kwargs) -> Response:
        """
        Update a MAC address in the designated switch's MAC address table.

        Example request: curl -X PUT -d '{"mac" : "00:00:00:00:00:01", "port" : 1}' http://127.0.0.1:8080/gelante/mactable/0000000000000001
        Expected Return: {"00:00:00:00:00:01": 1}
        Note: The expected return assumes the MAC address table was empty. Will return all entries.

        :param req: A request containing the MAC address entries you want to add to the MAC address table
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch to which you want to add
                       MAC address information.
        :return: Returns an updated version of the MAC address table if successful or an appropriate error message.
        """

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])
        try:
            new_entry = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)

        if dpid not in switch_instance.mac_to_port:
            return Response(status=404)

        # noinspection PyBroadException
        try:
            mac_table = switch_instance.set_mac_to_port(dpid, new_entry)
            body = json.dumps(mac_table)
            return Response(content_type='application/json', text=body)
        except Exception:
            return Response(status=500)

    @route('/gelante', '/gelante/inports/{dpid}', methods=['GET', 'PUT', 'OPTIONS'])
    def update_inports(self, req: json, **kwargs) -> Response:
        """
        Update the input ports on the switch.

        Example request: curl -X PUT -d '{"operation": "<add|delete>", "openflow_port": <openflow_port>}' http://127.0.0.1:8080/gelante/inports/150013889525632
        Example request: curl -X GET -d http://127.0.0.1:8080/gelante/inports/150013889525632

        :param req: A request containing the in port you want to add to traffic shaper's input ports. If a GET request
                    is used it will instead return a list of the current inports
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch to which you want to add
                       or retrieve input port information
        :return: Returns an updated version of the switch's input ports or the current list of inports
        """

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])

        if req.headers.environ.get("REQUEST_METHOD") == "OPTIONS":
            return create_response(req)

        if req.headers.environ.get("REQUEST_METHOD") == "GET":
            create_response(req, json.dumps(switch_instance.in_ports.get(dpid, [])))

        try:
            entry = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)

        openflow_port = entry.get("openflow_port", None)  # type: int
        operation = entry.get("operation", None).lower()  # type: str

        if operation != "add" and operation != "delete":
            return Response(status=400)

        if isinstance(operation, str) and isinstance(openflow_port, int):
            # noinspection PyBroadException
            try:
                if operation == "add":

                    if openflow_port not in switch_instance.in_ports.get(dpid, []):
                        switch_instance.in_ports[dpid].append(openflow_port)
                    body = json.dumps(switch_instance.in_ports)
                    return create_response(req, body)

                elif entry.get("operation") == "delete":

                    if openflow_port in switch_instance.in_ports.get(dpid, []):
                        switch_instance.in_ports[dpid].remove(openflow_port)
                    body = json.dumps(switch_instance.in_ports)
                    return create_response(req, body)

            except Exception:
                return Response(status=500)
        else:
            raise Response(status=400)

    @route('/gelante', '/gelante/outports/{dpid}', methods=['GET', 'PUT', 'OPTIONS'])
    def update_outports(self, req: json, **kwargs) -> Response:
        """
        Update the output ports on the switch.

        Example request: curl -X PUT -d '{"operation": "<add|delete>", "openflow_port": <openflow_port>}' http://127.0.0.1:8080/gelante/outports/150013889525632
        Example request: curl -X GET -d http://127.0.0.1:8080/gelante/outports/150013889525632

        :param req: A request containing the out port you want to modify. Valid operations include add and delete.
                    If the REQUEST_METHOD is GET it will instead send a list of the current output ports
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch to which you want to add
                       or retrieve output port information
        :return: Returns an updated version of the switch's output ports or a list of the current output ports
        """

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])

        if req.headers.environ.get("REQUEST_METHOD") == "OPTIONS":
            return create_response(req)

        if req.headers.environ.get("REQUEST_METHOD") == "GET":
            return create_response(req, json.dumps(switch_instance.out_ports.get(dpid, [])))

        try:
            entry = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)

        openflow_port = entry.get("openflow_port", None)  # type: int
        operation = entry.get("operation", None).lower()  # type: str

        if operation != "add" and operation != "delete":
            return Response(status=400)

        if isinstance(operation, str) and isinstance(openflow_port, int):
            # noinspection PyBroadException
            try:
                if operation == "add":

                    if openflow_port not in switch_instance.out_ports.get(dpid, []):
                        switch_instance.out_ports[dpid].append(openflow_port)
                    body = json.dumps(switch_instance.out_ports)
                    return create_response(req, body)

                elif entry.get("operation") == "delete":

                    if openflow_port in switch_instance.out_ports.get(dpid, []):
                        switch_instance.out_ports[dpid].remove(openflow_port)
                    body = json.dumps(switch_instance.out_ports)
                    return create_response(req, body)

            except Exception:
                return Response(status=500)
        else:
            raise Response(status=400)

    @staticmethod
    def _get_redirect_port_matches(tcp_port: int, udp_port: int, out_port: int) -> tuple:
        """
        This is a utility function used to create the OpenFlow matching rules required for port redirection

        :param tcp_port: The TCP port you would like to redirect to a switchport
        :param udp_port: The UDP port you would like to redirect to a switchport
        :param out_port: The switchport to which you would like to redirect
        :return:
        """

        if isinstance(tcp_port, int) and isinstance(out_port, int):

            match_in = OFPMatch(
                eth_type=int("800", 16),
                ip_proto=6,
                tcp_dst=tcp_port)

            match_out = OFPMatch(
                eth_type=int("800", 16),
                ip_proto=6,
                tcp_src=tcp_port)

        elif isinstance(udp_port, int) and isinstance(out_port, int):

            match_in = OFPMatch(
                eth_type=int("800", 16),
                ip_proto=17,
                udp_dst=udp_port)

            match_out = OFPMatch(
                eth_type=int("800", 16),
                ip_proto=17,
                udp_src=udp_port)
        else:
            return None, None

        return match_in, match_out

    def _delete_old_port_redirects(self, out_port: int, dpid: int):
        """
        Deletes all of the previous port redirects for a specified output port.

        :param out_port: The output port for which you want to delete the previous port redirects
        :param dpid: The DPID of the switch which you want to modify
        """

        tcp_udp_flows = get_tcp_udp_flows("ANY", out_port, dpid)
        tcp_udp_flows_match_patterns = []

        for flow in tcp_udp_flows:

            if "tp_src" in flow["match"]:
                port = flow["match"]["tp_src"]
            elif "tp_dst" in flow["match"]:
                port = flow["match"]["tp_dst"]
            else:
                logging.error("Whoops. We should never have gotten here. We couldn't find tp_dst or tp_src in the match "
                              "structure. Maybe the code changed?")
                return Response(status=500)

            if flow["match"]["nw_proto"] == 6:
                for match in GelanteController._get_redirect_port_matches(port, None, out_port):
                    tcp_udp_flows_match_patterns.append(match)

            elif flow["match"]["nw_proto"] == 17:
                for match in GelanteController._get_redirect_port_matches(None, port, out_port):
                    tcp_udp_flows_match_patterns.append(match)

            else:
                logging.error("Whoops. We should never have gotten here. We didn't find the TCP or UDP ip_protos in the"
                              "match structure. Maybe the code changed?")
                return Response(status=500)

        # TODO all the flows are actutually deleted twice because _get_redirect_port_matches gives you both send and
        # TODO receive. That said, it's such a minor amount of traffic I'm not fixing it right now
        logging.info("Deleting old entries for port " + str(out_port))
        for flow in tcp_udp_flows_match_patterns:
            delete_flow(self.gelante_app.get_datapath(dpid), flow, out_port)

    @route('/gelante', '/gelante/redirectport/{dpid}', methods=['PUT', 'OPTIONS'])
    def redirectport(self, req: json, **kwargs) -> Response:
        """
        Redirect flows coming in on a certain UDP/TCP port to go to a specific sensor. This will apply whether the given
        port is the source or the destination.

        Example request: curl -X PUT -d '{"operation": "<add|delete>", "<tcp_port|udp_port>" : <port#>, "out_port" : <openflow_port>}' http://127.0.0.1:8080/gelante/redirectport/150013889525632
        Example request: curl -X PUT -d '{"operation": "set", "ports" : "1/tcp,2/udp,3/tcp", "out_port" : <openflow_port>}' http://127.0.0.1:8080/gelante/redirectport/150013889525632

        Note: The expected return assumes the MAC address table was empty. Will return all entries.

        :param req: A request containing the L4 port you want to redirect and the output port to which you want to
                    redirect. Valid operations include delete, add, and set. Delete and add each act on a single port.
                    Set will delete the switchport's existing configuration and overwrite it with a new list of ports.
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch you want to modify
        :return: Returns an updated version of the L4 port -> output port mappings.
        """

        # TODO NEED TO ACCOUNT FOR AN EMPTY DATA STRING

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])

        if req.headers.environ.get("REQUEST_METHOD") == "OPTIONS":
            return create_response(req)

        try:
            entry = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)

        operation = entry.get("operation", None).lower()  # type: str
        out_port = entry.get("out_port", None)  # type: int
        tcp_port = entry.get("tcp_port", None)  # type: int
        udp_port = entry.get("udp_port", None)  # type: int
        ports = entry.get("ports", None)  # type []

        if operation != "add" and operation != "delete" and operation != "set":
            logging.error("Operation " + str(operation) + " is not a valid operation!")
            return Response(status=400)

        if not isinstance(out_port, int):
            logging.error("Output port " + str(out_port) + " is not an integer. Did you "
                                                           "accidentally add quotes?")
            return Response(status=400)

        # noinspection PyBroadException
        try:

            datapath = switch_instance.get_datapath(dpid)
            if datapath is not None:
                if operation == "add" or operation == "delete":

                    match_in, match_out = GelanteController._get_redirect_port_matches(tcp_port, udp_port, out_port)

                    if match_out is not None and match_in is not None:

                        actions = [OFPActionOutput(out_port)]

                        # First delete any previous flows for this specific port.
                        delete_flow(datapath, match_in)
                        delete_flow(datapath, match_out)
                        logging.debug("Deleting old flow rules for port.")

                        if operation == "add":
                            # Add the new flows.
                            add_flow(datapath, 1, match_in, actions, 300, 0)
                            add_flow(datapath, 1, match_out, actions, 300, 0)
                            logging.debug("Added new port rules.")

                        return Response(status=200)

                    else:
                        logging.error("Something went wrong in _get_redirect_port_matches. We tried to create"
                                      "match rules, but were unable to.")

                if operation == "set":

                    normalized_ports = []  # type: [tuple]

                    if isinstance(ports, str):

                        if ports != "":
                            ports_str = ports.strip().split(',')
                            for port in ports_str:
                                port_number_str, port_type = tuple(port.split('/'))
                                port_number = int(port_number_str)
                                port_number_str = port_number_str.lower()

                                if port_number < 1 or port_number > 65535:
                                    logging.error("Port " + port_number_str + " is not a valid port between 1 and 65535.")
                                    return Response(status=400)

                                if port_type != "tcp" and port_type != "udp":
                                    logging.error(port_number_str + " is not a valid port type. Must be \"tcp\" or \"udp\".")
                                    return Response(status=400)

                                normalized_ports.append((port_number, port_type))
                        else:
                            normalized_ports = None

                    else:
                        logging.error("Error. The ports you sent were not in a string format. Did you forget quotes?")
                        return Response(status=400)

                    if normalized_ports:
                        self._delete_old_port_redirects(out_port, dpid)

                        for port in normalized_ports:

                            port_number, port_type = port

                            if isinstance(port_number, int):

                                if port_type == "tcp":
                                    match_in, match_out = GelanteController._get_redirect_port_matches(port_number, None,
                                                                                                       out_port)
                                elif port_type == "udp":
                                    match_in, match_out = GelanteController._get_redirect_port_matches(None, port_number,
                                                                                                       out_port)

                                if match_out is not None and match_in is not None:

                                    actions = [OFPActionOutput(out_port)]

                                    add_flow(datapath, 1, match_in, actions, 300, 0)
                                    add_flow(datapath, 1, match_out, actions, 300, 0)
                                    logging.debug("Added new port rules.")

                                else:
                                    logging.error("Something went wrong in _get_redirect_port_matches. We tried to create"
                                                  "match rules, but were unable to.")

                            else:
                                logging.warning(str(port) + " is not an integer value. We are skipping it. Make sure "
                                                "you did not quote your values accidentally making them str instead of"
                                                " int.")
                    else:
                        self._delete_old_port_redirects(out_port, dpid)

                    body = {}
                    return create_response(req, json.dumps(body))

        except Exception as e:
            logging.error("We received error " + str(e))
            return Response(status=500)

    @route('/gelante', '/gelante/getports/{dpid}', methods=['GET'])
    def getports(self, req: json, **kwargs) -> Response:
        """
        Get a listing of all the OpenFlow port ID / switch port name combinations.

        Example request: curl -X GET -d http://127.0.0.1:8080/gelante/getports/150013889525632

        :param req: Used to generate the appropriate CORs headers, but otherwise unused in this function.
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch you want to modify
        :return: Returns a list of tuples in the form of (<openflow_port_id>: int, <switch_port_name>: string>)
        """

        switch_instance = self.gelante_app
        dpid = int(kwargs['dpid'])

        port_list = []

        for port, port_info in switch_instance.dpset.port_state[dpid].items():
            if port in switch_instance.out_ports[dpid]:
                role = "outport"
            elif port in switch_instance.in_ports[dpid]:
                role = "inport"
            else:
                role = "unassigned"

            port_list.append(
                {"hw_addr": port_info.hw_addr, "name": port_info.name.decode("utf-8"), "openflow_port": port,
                 "role": role, "redirects": get_tcp_udp_flows("ANY", port, dpid)})

        # Sort the ports by openflow port order - this corresponds to their order on the switch as well
        port_list = sorted(port_list, key=lambda i: i["openflow_port"])

        body = json.dumps(port_list)

        return create_response(req, body)

    # TODO - I used half a bracket on path. If you add the other half it breaks. Did I just accidentally hack webobs?
    # TODO - It probably shouldn't work like this.
    @route('/gelante', '/gelante/ryuapi/{path', methods=['GET', 'PUT', 'OPTIONS'])
    def ryuapi(self, req: json, **kwargs) -> Response:

        if req.headers.environ.get("REQUEST_METHOD") == "OPTIONS":
            return create_response(req)

        http = urllib3.PoolManager()

        response = http.request('GET', 'http://127.0.0.1:8080/' + kwargs["path"])

        return create_response(req, json.dumps(json.loads(response.data.decode('utf-8'))), response.headers['Content-Type'])


def main():
    sys.argv.append('--ofp-tcp-listen-port')
    sys.argv.append('6633')  # The port on which you want the controller to listen.
    sys.argv.append('main')  # This is the name of the Ryu app
    sys.argv.append('--verbose')
    sys.argv.append('--enable-debugger')
    manager.main()


if __name__ == '__main__':
    main()
