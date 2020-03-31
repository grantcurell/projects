__author__ = "Grant Curell"
__copyright__ = "Do what you want with it"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Grant Curell"

"""
An OpenFlow 1.3 L2 learning switch implementation.
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from pprint import PrettyPrinter
from ryu.cmd import manager
import sys


class LoadBalancer(app_manager.RyuApp):
    """
    This is the main Ryu app that is the Ryu controller

    In order to implement as a Ryu application, ryu.base.app_manager.RyuApp is inherited. Also, to use OpenFlow 1.3, the
    OpenFlow 1.3 version is specified for OFP_VERSIONS.

    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]


    def __init__(self, *args, **kwargs):
        super(LoadBalancer, self).__init__(*args, **kwargs)
        # mac_to_port is the MAC address table for the switch
        self.mac_to_port = {}


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

        :param datapath:
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


    def new_conversation(self, pkt):
        print("NEW CONVO")


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
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

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


def main():
    sys.argv.append('--ofp-tcp-listen-port')
    sys.argv.append('6633')  # The port on which you want the controller to listen.
    sys.argv.append('main')  # This is the name of the Ryu app
    sys.argv.append('--verbose')
    sys.argv.append('--enable-debugger')
    manager.main()


if __name__ == '__main__':
    main()
