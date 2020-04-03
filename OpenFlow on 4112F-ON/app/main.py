__author__ = "Grant Curell"
__copyright__ = "Do what you want with it"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Grant Curell"

"""
An OpenFlow 1.3 L2 learning switch implementation.
"""

import json
import sys
import communityid

from webob import Response
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller import dpset
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.app.wsgi import WSGIApplication, route
from ryu.app.ofctl_rest import StatsController,RestStatsApi
from pprint import PrettyPrinter # TODO REMOVE
from ryu.cmd import manager

simple_switch_instance_name = 'simple_switch_api_app'
url = '/simpleswitch/mactable/{dpid}'


class SimpleSwitch:
    """
    This is the main Ryu app that is the Ryu controller

    In order to implement as a Ryu application, ryu.base.app_manager.RyuApp is inherited. Also, to use OpenFlow 1.3, the
    OpenFlow 1.3 version is specified for OFP_VERSIONS.

    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        # mac_to_port is the MAC address table for the switch
        self.mac_to_port = {}
        self.flow_table = {}
        self.switches = {}

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
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]

        # Clear out all existing flows on the switch before continuing
        self.remove_all_flows(datapath)

        # Finally, 0 (lowest) is specified for priority and the add_flow() method is executed to send the Flow Mod
        # message. The content of the add_flow() method is explained in a later section.
        self.add_flow(datapath, 0, match, actions)


    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto

        # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
        # module. ryu.ofproto.ofproto_v1_3_parser
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        # The class corresponding to the Flow Mod message is the OFPFlowMod class. The instance of the OFPFlowMod
        # class is generated and the message is sent to the OpenFlow switch using the Datapath.send_msg() method.
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)


    def remove_all_flows(self, datapath):
        """
        Removes all the flows from the switch.

        :param datapath: Contains the information about the switch from which we want to remove flows
        :return:
        """

        match = datapath.ofproto_parser.OFPMatch()
        mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, datapath.ofproto.OFPTT_ALL,
                                         datapath.ofproto.OFPFC_DELETE,
                                         0, 0, 0, 0xffffffff,
                                         datapath.ofproto.OFPP_ANY,
                                         datapath.ofproto.OFPG_ANY,
                                         0, match, [])

        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """
        See https://osrg.github.io/ryu-book/en/html/switching_hub.html#event-handler for description.

        This function handles the ryu.controller.handler.MAIN_DISPATCHER state. This state is used to handle a new
        inbound packet

        :param ev: The event containing the packet data.
        :return:
        """

        msg = ev.msg
        # TODO remove when done
        # pp = PrettyPrinter(indent=4)
        # p.pprint(msg)
        datapath = msg.datapath
        ofproto = datapath.ofproto

        # Same as ofproto, indicates the ofproto_parser module. In the case of OpenFlow 1.3 format will be following
        # module. ryu.ofproto.ofproto_v1_3_parser
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id  # 64-bit OpenFlow Datapath ID of the switch to which the port belongs.

        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        """
        if len(pkt.protocols) > 3:
            print("here")

            if "ipv4" in pkt.protocols and "tcp" in pkt.protocols:
                cid = communityid.CommunityID()
                tpl = communityid.FlowTuple.make_tcp(pkt.protocols["ipv4"].src, pkt.protocols["ipv4"].dst, pkt.protocols["tcp"].src_port, pkt.protocols["tcp"].dst_port)
                flow_hash = cid.calc(tpl)

                if flow_hash in self.flow_table:
        """

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        self.logger.info("packet in %s %s %s", dpid, src, dst)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:

            # Unlike the Table-miss flow entry, set conditions for match this time. Implementation of the switching hub
            # this time, the receive port (in_port) and destination MAC address (eth_dst) have been specified. For
            # example, packets addressed to host B received by port 1 is the target.
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)

            # For the flow entry this time, the priority is specified to 1. The greater the value, the higher the
            # priority, therefore, the flow entry added here will be evaluated before the Table-miss flow entry.
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)

        # TODO remove when done
        # pp.pprint("Out is: " + str(out))
        datapath.send_msg(out)


class SimpleSwitchRest(SimpleSwitch, RestStatsApi):
    """
    Overview is here: https://osrg.github.io/ryu-book/en/html/rest_api.html

    This class extends the SimpleSwitch class above in order to add a REST API functionality.

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
        # passed in the key name simple_switch_api_app so that the constructor of the controller can access the instance
        # of the SimpleSwitchRest class.
        wsgi.register(SimpleSwitchController, {simple_switch_instance_name: self})
        SimpleSwitch.__init__(self, *args, **kwargs)
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

        super(SimpleSwitchRest, self).switch_features_handler(ev) # Call the original switch features method
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        self.mac_to_port.setdefault(datapath.id, {})

    def set_mac_to_port(self, dpid: int, entry: json):
        """
        Registers a pair of MAC address and port number in the MAC address table and adds a flow entry to the switch.
        The method is executed when REST API is called by the PUT method.

        :param dpid: 64-bit OpenFlow Datapath ID of the switch to which the port belongs.
        :param entry: A JSON entry including the MAC address and port pair you want to store
        :return:
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
                    self.add_flow(datapath, 1, match, actions)

                    # from new device to known device
                    actions = [parser.OFPActionOutput(port)]
                    match = parser.OFPMatch(in_port=entry_port, eth_dst=mac)
                    self.add_flow(datapath, 1, match, actions)

                mac_table.update({entry_mac: entry_port})
        return mac_table


class SimpleSwitchController(StatsController):

    _CONTEXTS = {
        'wsgi': WSGIApplication,
        'dpset': dpset.DPSet
    }

    def __init__(self, req, link, data, **config):
        data["dpset"] = data[simple_switch_instance_name].dpset

        # waiters in this case is ultimately used by ofctl_utils.py. It appears to be used for locks
        data["waiters"] = {}
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[simple_switch_instance_name]

    @route('/simpleswitch', url, methods=['GET'])
    def list_mac_table(self, req, **kwargs) -> Response:
        """
        Retrieves and returns the MAC address table of the specified switch. The REST API is called by the URL
        specified by the second argument. If the HTTP method at that time is GET, the list_mac_table method is called.
        This method acquires the MAC address table corresponding to the data path ID specified in the {dpid} part,
        converts it to the JSON format and returns it to the caller. If the data path ID of an unknown switch, which is
         not connected to Ryu, is specified, response code 404 is returned.
        
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch from which you want to dump
                       the MAC address table
        :return: Returns JSON containing the MAC address table of the specified switch.
        """

        simple_switch = self.simple_switch_app
        dpid = int(kwargs['dpid'])

        if dpid not in simple_switch.mac_to_port:
            return Response(status=404)

        mac_table = simple_switch.mac_to_port.get(dpid, {})
        body = json.dumps(mac_table)
        return Response(content_type='application/json', text=body)

    @route('/simpleswitch', url, methods=['PUT'])
    def put_mac_table(self, req: json, **kwargs) -> Response:
        """
        Update a MAC address in the designated switch's MAC address table.

        Example request: curl -X PUT -d '{"mac" : "00:00:00:00:00:01", "port" : 1}' http://127.0.0.1:8080/simpleswitch/mactable/0000000000000001
        Expected Return: {"00:00:00:00:00:01": 1}
        Note: The expected return assumes the MAC address table was empty. Will return all entries.

        :param req: A request containing the MAC address entries you want to add to the MAC address table
        :param kwargs: Expects an argument called dpid which contains the dpid of the switch to which you want to add
                       MAC address information.
        :return: Returns an updated version of the MAC address table if successful or an appropriate error message.
        """

        simple_switch = self.simple_switch_app
        dpid = int(kwargs['dpid'])
        try:
            new_entry = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)

        if dpid not in simple_switch.mac_to_port:
            return Response(status=404)

        # noinspection PyBroadException
        try:
            mac_table = simple_switch.set_mac_to_port(dpid, new_entry)
            body = json.dumps(mac_table)
            return Response(content_type='application/json', text=body)
        except Exception as e:
            return Response(status=500)


def main():
    sys.argv.append('--ofp-tcp-listen-port')
    sys.argv.append('6633')  # The port on which you want the controller to listen.
    sys.argv.append('main')  # This is the name of the Ryu app
    sys.argv.append('--verbose')
    sys.argv.append('--enable-debugger')
    manager.main()


if __name__ == '__main__':
    main()
