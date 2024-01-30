// Example program that tests whether GPUDirect RDMA functionality is working properly. It assumes that
// the system has two MLX5 devices that are connected to each other, either directly or via a switch. Using
// the libibverbs API, it then transmits a particular UDPv4 packet out of one port and looks to receive the 
// same packet on the other.
//
// Building:
//
// This program can be built using the following command line (tested on CentOS 8.5 with gcc 8.5.0):
//
//     g++ rdma-loopback.cpp -o rdma-loopback -libverbs -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -lcudart
//
// Usage:
//
//     ./rdma-loopback (no arguments)
//
// When invoked this way, the loopback test will be performed without using any CUDA device at all; the packets
// will be transmitted out of and received into system memory. This should always work, assuming a working
// MLNX_OFED installation.
//
//     ./rdma-loopback <CUDA device index>
//
// When invoked with a numeric argument, it is interpreted as the index of the CUDA device that should be used
// for GPUDirect RDMA. The packet will be transmitted out of system memory, just as described above. When a CUDA
// device is selected, though, a memory region on the CUDA device will be registered with the ibverbs API and the
// receive queue will be configured to write the received packet to that memory region. After receiving the packet,
// it is copied back to host memory for comparison against the expected pattern.
//
// NOTE: as this is just a proof of concept, all MLX5 device parameters are hard-coded in the source code below;
// they may need to be adjusted for the system under test.
//
#include <arpa/inet.h>
#include <cuda_runtime.h>
#include <infiniband/verbs.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <stdexcept>
#include <string>
#include <time.h>
#include <vector>
#include <iostream>
using namespace std;

ibv_device *find_device_by_ibv_name(const char *dev_name)
{
    // Iterate over all of the ibverbs devices that were found.
    int num_devices = 0;
    auto dev_list = ibv_get_device_list(&num_devices);
    ibv_device *device = nullptr;
    for (int i = 0; i < num_devices; ++i)
    { 
        /*
        cout << "HERE\n";
        cout << ibv_get_device_name(dev_list[i]); 
        cout << "\n";
        */
        if (!strcmp(dev_name, ibv_get_device_name(dev_list[i])))
        {
            device = dev_list[i];
            break;
        }
    }
    // Clean up the device list.
    if (dev_list) ibv_free_device_list(dev_list);
    // Return the device we found, if any.
    return device;
}

uint32_t ipv4_from_string(const char *s)
{
    in_addr addr;
    auto ret = inet_pton(AF_INET, s, &addr);
    if (ret != 1) throw std::runtime_error("invalid IPv4 address");
    return addr.s_addr;
}

// Constants used below.
size_t cq_len = 1;
size_t cq_vec = 0;

// UPDATE CODE HERE
// This is the MLX5 device
const char *rx_ibv_name = "mlx5_0";
size_t rx_port_num = 1;
// Receive MAC 0c:42:a1:73:8d:e6
uint8_t dest_mac_addr[] = { 0x0c, 0x42, 0xa1, 0x73, 0x8d, 0xe6 };
const char *dest_ipv4_addr_str = "10.1.100.1";
uint32_t dest_ipv4_addr = ipv4_from_string(dest_ipv4_addr_str);
uint16_t dest_udp_port = 12345;

// This is the MLX6 device
const char *tx_ibv_name = "mlx5_3";
size_t tx_port_num = 1;
// Transmit MAC: b8:ce:f6:cc:9e:dd
uint8_t src_mac_addr[] = { 0xb8, 0xce, 0xf6, 0xcc, 0x9e, 0xdd };
const char *src_ipv4_addr_str = "10.1.100.2";
uint32_t src_ipv4_addr = ipv4_from_string(src_ipv4_addr_str);
uint16_t src_udp_port = 12345;

size_t eth_hdr_len = 14;
size_t ip_hdr_len = 20;
size_t udp_hdr_len = 8;
size_t udp_payload_len = 32;
size_t packet_len = eth_hdr_len + ip_hdr_len + udp_hdr_len + udp_payload_len;

int main(int argc, const char *argv[])
{
    // Check to see if we got a second argument. If we did, it specifies the CUDA device index that we should place the receive buffer on.
    int cuda_dev_ind = -1;
    if (argc > 1)
    {
        cuda_dev_ind = strtol(argv[1], nullptr, 10);
        if ((cuda_dev_ind == LONG_MIN) || (cuda_dev_ind == LONG_MAX)) throw std::runtime_error("error parsing CUDA device index argument");
    }

    printf("setting up IBV RX device '%s'; destination MAC: %02x:%02x:%02x:%02x:%02x:%02x; destination UDP endpoint: %s:%u...\n",
        rx_ibv_name, dest_mac_addr[0], dest_mac_addr[1], dest_mac_addr[2], dest_mac_addr[3], dest_mac_addr[4], dest_mac_addr[5],
        dest_ipv4_addr_str, dest_udp_port);

    // First, set up the receiving interface.
    auto rx_device = find_device_by_ibv_name(rx_ibv_name);
    if (!rx_device) throw std::runtime_error("error finding RX device");

    auto rx_context = ibv_open_device(rx_device);
    if (!rx_context) throw std::runtime_error("error creating RX device context");

    auto rx_pd = ibv_alloc_pd(rx_context);
    if (!rx_pd) throw std::runtime_error("error creating RX protection domain");

    auto rx_cq = ibv_create_cq(rx_context, cq_len, nullptr, nullptr, cq_vec);
    if (!rx_cq) throw std::runtime_error("error creating RX completion queue");

    // This creates a queue pair (QP) associated with a protection domain pd. The argument qp_init_attr_ex is an
    // ibv_qp_init_attr_eq struct, as defined in <infiniband/verbs.h>. A queue pair is roughly the same as a
    // socket.
    ibv_qp_init_attr_ex rx_qp_init_attr;
    memset(&rx_qp_init_attr, 0, sizeof(rx_qp_init_attr));
    rx_qp_init_attr.cap.max_recv_wr = cq_len;
    rx_qp_init_attr.cap.max_recv_sge = 1;
    rx_qp_init_attr.send_cq = rx_cq;
    rx_qp_init_attr.recv_cq = rx_cq;
    rx_qp_init_attr.cap.max_inline_data = 0;
    rx_qp_init_attr.qp_type = IBV_QPT_RAW_PACKET;
    rx_qp_init_attr.sq_sig_all = 1;
    rx_qp_init_attr.comp_mask = IBV_QP_INIT_ATTR_PD | IBV_QP_INIT_ATTR_CREATE_FLAGS;
    rx_qp_init_attr.pd = rx_pd;
    auto rx_qp = ibv_create_qp_ex(rx_context, &rx_qp_init_attr);
    if (!rx_qp) throw std::runtime_error("error creating RX queue pair");

    // Initialize its state machine as described in the documentation for `ibv_modify_qp()` for raw Ethernet operation.
    ibv_qp_attr rx_qp_attr;
    memset(&rx_qp_attr, 0, sizeof(&rx_qp_attr));
    rx_qp_attr.qp_state = IBV_QPS_INIT;
    rx_qp_attr.port_num = rx_port_num;
    if (auto err = ibv_modify_qp(rx_qp, &rx_qp_attr, IBV_QP_STATE | IBV_QP_PORT))
        throw std::runtime_error("error initializing state of RX queue pair");

    memset(&rx_qp_attr, 0, sizeof(&rx_qp_attr));
    rx_qp_attr.qp_state = IBV_QPS_RTR;
    if (auto err = ibv_modify_qp(rx_qp, &rx_qp_attr, IBV_QP_STATE))
        throw std::runtime_error("error setting ready to read on RX queue pair");

    // Create a flow that will steer the requested flow to this queue. We need a buffer to encode all of the data that we pass to the API.
    auto buf_size = sizeof(ibv_flow_attr) + sizeof(ibv_flow_spec_ipv4) + sizeof(ibv_flow_spec_tcp_udp);
    std::vector<uint8_t> buf(buf_size);
    // Populate the header.
    auto fa = reinterpret_cast<ibv_flow_attr *>(&buf[0]);
    memset(fa, 0, sizeof(ibv_flow_attr));
    fa->type = IBV_FLOW_ATTR_NORMAL;
    fa->size = sizeof(ibv_flow_attr);
    fa->num_of_specs = 2;
    fa->port = rx_port_num;
    // Add the IPv4 destination address steering rule.
    auto ia = reinterpret_cast<ibv_flow_spec_ipv4 *>(fa + 1);
    memset(ia, 0, sizeof(ibv_flow_spec_ipv4));
    ia->type = IBV_FLOW_SPEC_IPV4;
    ia->size = sizeof(ibv_flow_spec_ipv4);
    ia->val.dst_ip = dest_ipv4_addr;
    ia->mask.dst_ip = 0xffffffff;
    // Add the UDP port steering rule.
    auto ua = reinterpret_cast<ibv_flow_spec_tcp_udp *>(ia + 1);
    memset(ua, 0, sizeof(ibv_flow_spec_tcp_udp));
    ua->type = IBV_FLOW_SPEC_UDP;
    ua->size = sizeof(ibv_flow_spec_tcp_udp);
    ua->val.dst_port = htons(dest_udp_port);
    ua->mask.dst_port = 0xffff;
    // Create the flow.
    auto flow = ibv_create_flow(rx_qp, fa);
    if (!flow) throw std::runtime_error("couldn't create steering rule for UDP flow");

    // Allocate memory that we will receive packets into.
    std::vector<uint8_t> rx_buf(packet_len);
    // Fill it with a pattern initially to help us know whether it gets overwritten properly.
    for (size_t i = 0; i < packet_len; ++i) rx_buf[i] = 0xaa;

    void *cuda_rx_buf = nullptr;
    if (cuda_dev_ind >= 0)
    {
        printf("registering CUDA device memory region for RX...\n");
        cudaDeviceProp prop;
        auto ret = cudaGetDeviceProperties(&prop, cuda_dev_ind);
        if (ret != cudaSuccess) throw std::runtime_error("couldn't get CUDA device properties");
        printf("    CUDA device index: %u; name: %s\n", cuda_dev_ind, prop.name);
        // Select the specified CUDA device.
        ret = cudaSetDevice(cuda_dev_ind);
        if (ret != cudaSuccess) throw std::runtime_error("couldn't select CUDA device");
        // Allocate the block of device memory.
        ret = cudaMalloc(&cuda_rx_buf, rx_buf.size());
        if (ret != cudaSuccess) throw std::runtime_error("couldn't allocate CUDA memory region");
        // Fill the device memory with a different pattern from the host buffer so we know what state it begins in.
        ret = cudaMemset(cuda_rx_buf, 0x55, packet_len);
        if (ret != cudaSuccess) throw std::runtime_error("couldn't fill CUDA memory region");
    }
    else printf("registering host memory region for RX...\n");

    // Register the memory region.
    void *actual_rx_buf = cuda_rx_buf ? cuda_rx_buf : &rx_buf[0];
    // ibv_reg_mr() registers a memory region (MR) associated with the protection domain pd. The MR's starting address is
    // addr and its size is length. The argument access describes the desired memory protection attributes;
    // it is either 0 or the bitwise OR of one or more flags (detailed online).
    auto rx_mr = ibv_reg_mr(rx_pd, actual_rx_buf, rx_buf.size(), IBV_ACCESS_LOCAL_WRITE);
    if (!rx_mr) throw std::runtime_error("couldn't register RX memory region");

    // Post a work request to receive a packet.
    ibv_sge rx_sge;
    rx_sge.addr = reinterpret_cast<uint64_t>(actual_rx_buf);
    rx_sge.length = rx_buf.size();
    rx_sge.lkey = rx_mr->lkey;

    ibv_recv_wr rx_wr;
    memset(&rx_wr, 0, sizeof(rx_wr));
    rx_wr.wr_id = 0;
    rx_wr.next = nullptr;
    rx_wr.sg_list = &rx_sge;
    rx_wr.num_sge = 1;

    ibv_recv_wr *bad_rx_wr;
    if (ibv_post_recv(rx_qp, &rx_wr, &bad_rx_wr)) throw std::runtime_error("error posting to RX queue");

    // -------------------------------------------------------------------------------------------------------------------------

    printf("setting up IBV TX device '%s'; source MAC: %02x:%02x:%02x:%02x:%02x:%02x; source UDP endpoint: %s:%u...\n",
        tx_ibv_name, src_mac_addr[0], src_mac_addr[1], src_mac_addr[2], src_mac_addr[3], src_mac_addr[4], src_mac_addr[5],
        src_ipv4_addr_str, src_udp_port);

    // Now, set up the transmit interface.
    auto tx_device = find_device_by_ibv_name(tx_ibv_name);
    if (!tx_device) throw std::runtime_error("error finding TX device");

    auto tx_context = ibv_open_device(tx_device);
    if (!tx_context) throw std::runtime_error("error creating TX device context");

    auto tx_pd = ibv_alloc_pd(tx_context);
    if (!tx_pd) throw std::runtime_error("error creating TX protection domain");

    auto tx_cq = ibv_create_cq(tx_context, cq_len, nullptr, nullptr, cq_vec);
    if (!tx_cq) throw std::runtime_error("error creating TX completion queue");

    ibv_qp_init_attr_ex tx_qp_init_attr;
    memset(&tx_qp_init_attr, 0, sizeof(tx_qp_init_attr));
    tx_qp_init_attr.cap.max_send_wr = cq_len;
    tx_qp_init_attr.cap.max_send_sge = 1;
    tx_qp_init_attr.send_cq = tx_cq;
    tx_qp_init_attr.recv_cq = tx_cq;
    tx_qp_init_attr.cap.max_inline_data = 0;
    tx_qp_init_attr.qp_type = IBV_QPT_RAW_PACKET;
    tx_qp_init_attr.sq_sig_all = 1;
    tx_qp_init_attr.comp_mask = IBV_QP_INIT_ATTR_PD | IBV_QP_INIT_ATTR_CREATE_FLAGS;
    tx_qp_init_attr.pd = tx_pd;
    auto tx_qp = ibv_create_qp_ex(tx_context, &tx_qp_init_attr);
    if (!tx_qp) throw std::runtime_error("error creating TX queue pair");

    // Initialize its state machine as described in the documentation for `ibv_modify_qp()` for raw Ethernet operation.
    ibv_qp_attr tx_qp_attr;
    memset(&tx_qp_attr, 0, sizeof(&tx_qp_attr));
    tx_qp_attr.qp_state = IBV_QPS_INIT;
    tx_qp_attr.port_num = tx_port_num;
    if (auto err = ibv_modify_qp(tx_qp, &tx_qp_attr, IBV_QP_STATE | IBV_QP_PORT))
        throw std::runtime_error("error initializing state of TX queue pair");

    memset(&tx_qp_attr, 0, sizeof(&tx_qp_attr));
    tx_qp_attr.qp_state = IBV_QPS_RTR;
    if (auto err = ibv_modify_qp(tx_qp, &tx_qp_attr, IBV_QP_STATE))
        throw std::runtime_error("error setting ready to read on TX queue pair");

    memset(&tx_qp_attr, 0, sizeof(&tx_qp_attr));
    tx_qp_attr.qp_state = IBV_QPS_RTS;
    if (auto err = ibv_modify_qp(tx_qp, &tx_qp_attr, IBV_QP_STATE))
        throw std::runtime_error("error setting ready to send on TX queue pair");

    // Allocate memory that we will send packets from.
    std::vector<uint8_t> tx_buf(packet_len);
    // Register the memory region.
    auto tx_mr = ibv_reg_mr(tx_pd, &tx_buf[0], tx_buf.size(), IBV_ACCESS_LOCAL_WRITE);
    if (!tx_mr) throw std::runtime_error("couldn't register TX memory region");

    // Start filling the packet buffer with the Ethernet header.
    auto eh = reinterpret_cast<ethhdr *>(&tx_buf[0]);
    memcpy(eh->h_dest, dest_mac_addr, sizeof(eh->h_dest));
    memcpy(eh->h_source, src_mac_addr, sizeof(eh->h_source));
    eh->h_proto = htons(ETH_P_IP);
    // Insert the IPv4 header.
    auto ip = reinterpret_cast<iphdr *>(eh + 1);
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 0;
    ip->tot_len = htons(packet_len - ETH_HLEN);
    ip->id = 0;
    ip->frag_off = 0;
    ip->ttl = 255;
    ip->protocol = IPPROTO_UDP;
    // The IPv4 checksum should be calculated by the hardware for us.
    ip->check = 0;
    ip->saddr = src_ipv4_addr;
    ip->daddr = dest_ipv4_addr;
    // Insert the UDP header.
    auto udp = reinterpret_cast<udphdr *>(ip + 1);
    udp->source = htons(src_udp_port);
    udp->dest = htons(dest_udp_port);
    udp->len = htons(packet_len - ETH_HLEN - ip_hdr_len);
    // The checksum should be filled in by the hardware.
    udp->check = 0;
    // Fill the payload with a pattern.
    auto payload = reinterpret_cast<char *>(udp + 1);
    for (int i = 0; i < udp_payload_len; ++i) payload[i] = i;

    // Post a work request to send the packet.
    ibv_sge tx_sge;
    tx_sge.addr = reinterpret_cast<uint64_t>(&tx_buf[0]);
    tx_sge.length = tx_buf.size();
    tx_sge.lkey = tx_mr->lkey;

    // This creates a send request (SR). An SR defines how much data will be sent, from where, how and, with RDMA, to where. struct
    // ibv_send_wr is used to implement SRs.
    ibv_send_wr tx_wr;
    memset(&tx_wr, 0, sizeof(tx_wr));
    tx_wr.wr_id = 0;
    tx_wr.next = nullptr;
    tx_wr.sg_list = &tx_sge;
    tx_wr.num_sge = 1;
    tx_wr.opcode = IBV_WR_SEND;
    tx_wr.send_flags = IBV_SEND_IP_CSUM;

    ibv_send_wr *bad_tx_wr;
    // ibv_post_send posts a linked list of Work Requests (WRs) to the send queue of a queue pair. ibv_post_send goes over all the entries
    // in the linked list one by one and checks if they are valid, generates an HW-specific send request from it and then adds that to the
    // tail of the QP's send queue without performing any contexting switching. If there is a failure in any of the work requests it will
    // stop immediately and return a pointer to that WR. 0 indicates success.
    auto result = ibv_post_send(tx_qp, &tx_wr, &bad_tx_wr); // This returns 0
    if (result) throw std::runtime_error("error posting to TX queue: error: " + std::string(strerror(errno)));

    // -------------------------------------------------------------------------------------------------------------------------

    printf("polling RX CQ...\n");

    // Poll the receive queue (for up to 1 second) to make sure we got the packet.
    int max_polls = 1000;
    int sleep_nsec = 1e3;
    while (max_polls--)
    {
        ibv_wc rx_wc;
        // Here, CQ refers to completion queue
        auto num_rx = ibv_poll_cq(rx_cq, 1, &rx_wc);
        if (num_rx > 0)
        {
            printf("received packet\n");
            // Make sure the received packet is correct.
            if (rx_wc.status == IBV_WC_SUCCESS)
            {
                // If we got the right length...
                if (rx_wc.byte_len == packet_len)
                {
                    // Copy the data to the host if needed.
                    if (actual_rx_buf == cuda_rx_buf) 
                    {
                        printf("copying packet from CUDA device memory to host...\n");
                        auto ret = cudaMemcpy(&rx_buf[0], cuda_rx_buf, packet_len, cudaMemcpyDeviceToHost);
                        if (ret != cudaSuccess) throw std::runtime_error("couldn't copy received packet from CUDA device");
                    }

                    // The transmit buffer doesn't have the IP/UDP checksums in it since they were calculated by the hardware. Copy those back
                    // to the transmit buffer before checking the packet contents.
                    size_t ip_checksum_offset = eth_hdr_len + ip_hdr_len - 2 * sizeof(uint32_t) - sizeof(uint16_t);
                    memcpy(&tx_buf[ip_checksum_offset], &rx_buf[ip_checksum_offset], sizeof(uint16_t));

                    size_t udp_checksum_offset = eth_hdr_len + ip_hdr_len + udp_hdr_len - sizeof(uint16_t);
                    memcpy(&tx_buf[udp_checksum_offset], &rx_buf[udp_checksum_offset], sizeof(uint16_t));

                    // At this point, `tx_buf` and `rx_buf` should hold identical contents.                    
                    printf("tx: ");
                    for (size_t i = 0; i < packet_len; ++i) printf("%02x ", tx_buf[i]);
                    printf("\n");
                    printf("rx: ");
                    for (size_t i = 0; i < packet_len; ++i) printf("%02x ", rx_buf[i]);
                    printf("\n");
                    if (tx_buf == rx_buf) 
                    {
                        printf("success\n");
                        return 0;
                    }
                    else 
                    {
                        printf("failure\n");
                        return 1;
                    }
                }
                else throw std::runtime_error("packet received with wrong length");
            }
            else throw std::runtime_error("packet received with error");
            // Break out of the wait loop.
            break;
        }
        else if (num_rx < 0) throw std::runtime_error("error polling RX completion queue");
        // Wait a bit before polling again.
        timespec wait_time;
        wait_time.tv_sec = 0;
        wait_time.tv_nsec = sleep_nsec;
        nanosleep(&wait_time, nullptr);
    }
    if (!max_polls) throw std::runtime_error("timeout waiting for RX packet");
}
