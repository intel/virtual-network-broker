/*
#    Copyright (c) 2016 Intel Corporation.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
 */

#ifndef _FILTERAGENT_H
#define _FILTERAGENT_H

/** @file
 * Secmonagent header
 * 
 */

#include <stdio.h>
#include <pthread.h>
#include <rte_log.h>
#include <stdlib.h>
#include <string.h>
#include <sched.h>
#include <stdint.h>
#include <signal.h>
#include <dlfcn.h>
#include <dirent.h>
#include <inttypes.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <syslog.h>
#include <sys/queue.h>
#include <netinet/in.h>
#include <setjmp.h>
#include <stdarg.h>
#include <ctype.h>
#include <errno.h>
#include <poll.h>
#include <sys/inotify.h>
#include <getopt.h>
#include <endian.h>
#include <rte_common.h>
#include <rte_log.h>
#include <rte_memory.h>
#include <rte_memcpy.h>
#include <rte_memzone.h>
#include <rte_eal.h>
#include <rte_per_lcore.h>
#include <rte_launch.h>
#include <rte_atomic.h>
#include <rte_cycles.h>
#include <rte_prefetch.h>
#include <rte_lcore.h>
#include <rte_per_lcore.h>
#include <rte_branch_prediction.h>
#include <rte_interrupts.h>
#include <rte_pci.h>
#include <rte_random.h>
#include <rte_debug.h>
#include <rte_ether.h>
#include <rte_ethdev.h>
#include <rte_ring.h>
#include <rte_mempool.h>
#include <rte_mbuf.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/socket.h> 
#include <unistd.h>    
#include <dirent.h>

#define MBUF_SIZE (2048 + sizeof(struct rte_mbuf) + RTE_PKTMBUF_HEADROOM)
#define NB_MBUF   			8192
#define DPDK_CORE_ID 		1	
#define MAX_PKT_BURST 		32
#define BURST_TX_DRAIN_US 	100 /* TX drain every ~100us */
#define MAX_EVENT_LENGTH    4096
#define CHECK_INTERVAL 		100 /* 100ms */
#define MAX_CHECK_TIME 		90 	/* 9s (90 * 100ms) in total */
/*
 * Configurable number of RX/TX ring descriptors
 */
#define RTE_TEST_RX_DESC_DEFAULT	128
#define RTE_TEST_TX_DESC_DEFAULT 	512
#define TIMER_MILLISECOND 			2000000ULL	/* around 1ms at 2 Ghz */
#define MAX_TIMER_PERIOD 			86400 		/* 1 day max */
#define MAX_RX_QUEUE_PER_LCORE 		16
#define MAX_TX_QUEUE_PER_PORT 		16
#define MILLISEC_TO_SEC 			1000
#define MSG_SIZE 					4096
#define CONF_KEY 		100
#define MAC_SHIFT_LEN 	36
#define MAC_HEADER_LEN 	14
#define VLAN_HEADER_LEN 4
#define MAC_VLAN_HDR    MAC_HEADER_LEN+VLAN_HEADER_LEN
#define IPV4_HDR_LEN 	20
#define IPV4_L4_HDR_OFFSET MAC_HEADER_LEN + IPV4_HDR_LEN 
#define VLAN 			0x8100
#define IPV4_PACKET 	0x0800
#define IPV6_PACKET 	0x86DD
#define ARP_PACKET 		0x0806
#define PROTO_GTP 		2152

#define ETHER_ADDR_LEN 	6
#define IPV6_ADDR_LEN 	80
#define IPV4_ADDR_LEN 	16
#define MAX_ID_LEN 		80
#define MAX_IP_LEN 		80
#define MAX_NAME_LEN 	80

#define FILE_EXTN_LEN 3 //.so file extension

#define SUCCESS 0
#define FAILURE -1
#define INVALID 0

#define MAX_PLUGINS 100

struct hw_addr
{
    uint8_t addr[ETHER_ADDR_LEN];
} __attribute__((__packed__));

struct ether_header
{
    struct hw_addr dst_mac; /**< destination mac */
    struct hw_addr src_mac; /**< source mac */
    uint16_t ether_type;  /**< ether type */
} __attribute__((__packed__));

struct ipv4_header
{
    uint8_t  version_ihl;       /**< version and header length */
    uint8_t  type_of_service;   /**< type of service */
    uint16_t total_length;      /**< length of packet */
    uint16_t packet_id;     /**< packet ID */
    uint16_t fragment_offset;   /**< fragmentation offset */
    uint8_t  time_to_live;      /**< time to live */
    uint8_t  next_proto_id;     /**< protocol ID */
    uint16_t hdr_checksum;      /**< header checksum */
    uint32_t src_addr;      /**< source address */
    uint32_t dst_addr;      /**< destination address */
} __attribute__((__packed__));

struct ipv6_header
{
    uint32_t vtc_flow;
    uint16_t payload_len;
    uint8_t proto;
    uint8_t hop_limits;
    uint8_t src_addr[IPV6_ADDR_LEN];
    uint8_t dst_addr[IPV6_ADDR_LEN];
}__attribute__((__packed__));

struct tcp_header
{
    uint16_t src_port;  /**< TCP source port. */
    uint16_t dst_port;  /**< TCP destination port. */
    uint32_t sent_seq;  /**< TX data sequence number. */
    uint32_t recv_ack;  /**< RX data acknowledgment sequence number. */
    uint8_t  data_off;  /**< Data offset. */
    uint8_t  tcp_flags; /**< TCP flags */
    uint16_t rx_win;    /**< RX flow control window. */
    uint16_t cksum;     /**< TCP checksum. */
    uint16_t tcp_urp;   /**< TCP urgent pointer, if any. */
} __attribute__((__packed__));

struct icmp_header
{
    uint8_t  icmp_type;   /**< ICMP packet type. */
    uint8_t  icmp_code;   /**< ICMP packet code. */
    uint16_t icmp_cksum;  /**< ICMP packet checksum. */
    uint16_t icmp_ident;  /**< ICMP packet identifier. */
    uint16_t icmp_seq_nb; /**< ICMP packet sequence number. */
} __attribute__((__packed__));

struct udp_header {
    uint16_t src_port;    /**< UDP source port. */
    uint16_t dst_port;    /**< UDP destination port. */
    uint16_t dgram_len;   /**< UDP datagram length */
    uint16_t dgram_cksum; /**< UDP datagram checksum */
} __attribute__((__packed__));

struct ipv4_addresses
{
    uint32_t src_addr;
    uint32_t dst_addr;
} __attribute__((__packed__));

struct ipv6_addresses
{
    struct in6_addr src_addr;
    struct in6_addr dst_addr;
} __attribute__((__packed__));

static void send_packets(struct rte_mbuf *m);

static void plugin_loader(void);
static void watch_plugin_directory(void);
static void handle_file_event(int fd);
static void load_plugin(const char *path);
static void send_packets(struct rte_mbuf *m);
inline void shift_mac(char *,int );
void strip_gtp_header(struct rte_mbuf *m);


/** strips gtp header out of the packet.
 * @param 
 *  secmon_pkt pointer to the packet
 * @param 
 *  len        length of the packet
 * @returns void
 *       
 */

inline void shift_mac(char *pkt,int len)
{
    int i;
    for(i=0;i<len;i++)
    {
        *(pkt + MAC_SHIFT_LEN) = *(pkt);
        pkt++;
    }
}

#endif
