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

/** @file
 * 	Receives packets from dpdk interface and forwards the packets 
 * 	to loaded plugins(.so files). It can load plugins dynamically 
 * 	into the program
 */

#define _GNU_SOURCE
#include "SecMonAgent.h"

const char path[]="/opt/secmon/plugins";

static unsigned short nb_rxd = RTE_TEST_RX_DESC_DEFAULT;
static unsigned short nb_txd = RTE_TEST_TX_DESC_DEFAULT;

static unsigned int plugins=0;
/* A tsc-based timer responsible for triggering statistics printout */
static long int timer_period = 10 * TIMER_MILLISECOND * MILLISEC_TO_SEC; /* default period is 10 seconds */

/* Ethernet addresses of ports */
static struct ether_addr l2fwd_ports_eth_addr[RTE_MAX_ETHPORTS];

/* mask of enabled ports */
static unsigned int l2fwd_enabled_port_mask;

static unsigned int l2fwd_rx_queue_per_lcore = 1;

struct mbuf_table {
    unsigned len;
    struct rte_mbuf *m_table[MAX_PKT_BURST];
};

struct lcore_queue_conf {
    unsigned n_rx_port;
    unsigned rx_port_list[MAX_RX_QUEUE_PER_LCORE];
    struct mbuf_table tx_mbufs[RTE_MAX_ETHPORTS];

} __rte_cache_aligned;
struct lcore_queue_conf lcore_queue_conf[RTE_MAX_LCORE];

static const struct rte_eth_conf port_conf = {
    .rxmode = {
        .split_hdr_size = 0,
        .header_split   = 0, /**< Header Split disabled */
        .hw_ip_checksum = 0, /**< IP checksum offload disabled */
        .hw_vlan_filter = 0, /**< VLAN filtering disabled */
        .jumbo_frame    = 0, /**< Jumbo Frame Support disabled */
        .hw_strip_crc   = 0, /**< CRC stripped by hardware */
    },
    .txmode = {
        .mq_mode = ETH_MQ_TX_NONE,
    },
};

struct rte_mempool * l2fwd_pktmbuf_pool = NULL;

/* Per-port statistics struct */
struct l2fwd_port_statistics {
    uint64_t tx;
    uint64_t rx;
    uint64_t dropped;
} __rte_cache_aligned;
struct l2fwd_port_statistics port_statistics[RTE_MAX_ETHPORTS];



/* plugin api function pointers. */
void *handle;
int (*init)(void);
int (*config)(int);
int (*receive_data)(int);
int (*send_packet[MAX_PLUGINS])(struct rte_mbuf *);

/** Main processing loop. 
 *
 * Polls the dpdk interface for rx packets.
 * Process the packets for gtp header and strips it.
 * Forwards the processed packet to loaded plugins
 *
 * @param void
 * @return 
 * 	void
 */

static void receiver_thread(void)
{
    struct rte_mbuf *pkts_burst[MAX_PKT_BURST];
    struct rte_mbuf *m;
    unsigned lcore_id;
    unsigned i, j, portid, nb_rx;
    struct lcore_queue_conf *qconf;
    lcore_id = rte_lcore_id();
    qconf = &lcore_queue_conf[lcore_id];
    if (qconf->n_rx_port == 0) 
    {
        syslog(LOG_INFO|LOG_LOCAL0, "lcore %u has nothing to do\n", lcore_id);
        return;
    }

    for (i = 0; i < qconf->n_rx_port; i++) {

        portid = qconf->rx_port_list[i];
        syslog(LOG_INFO|LOG_LOCAL0, " -- lcoreid=%u port id=%u queue id=%d\n", lcore_id,
                portid,i);
    }

    while (1) 
    {
        /* Read packet from RX queues*/
        for (i = 0; i < qconf->n_rx_port; i++)
        {
            portid = qconf->rx_port_list[i];
            nb_rx = rte_eth_rx_burst((uint8_t) portid,i,pkts_burst,MAX_PKT_BURST);

            for (j = 0; j < nb_rx; j++) 
            {
                m = pkts_burst[j];

                /* pre-fetch a cache line to all cache levels */
                rte_prefetch0(rte_pktmbuf_mtod(m, void *));
                send_packets(m);
            }
            /* free the packet mbufs */
            for(j=0;j<nb_rx;j++)
                rte_pktmbuf_free(pkts_burst[j]);
        }
    }
}

/** sends the packet's rte_mbuf pointer to the loaded plugins 
 * and increments the atomic_refcnt variable as many times as plugins.
 * 
 * @param
 *     m - rte_mbuf pointer of the packet
 * @returns
 * 	   void
 */

static void send_packets(struct rte_mbuf *m)
{
    unsigned int n_plugins = plugins;

    while(n_plugins > 0)
    {
        /*strip gtp header from the packet for GTP-U de-tunneling*/
        strip_gtp_header(m);

        rte_mbuf_refcnt_update(m,1);
        (*send_packet[n_plugins-1])(m);
        n_plugins--;
    }
}

/** watches the directory /opt/secmon/plugins
 * for checking if a new plugin has been put in and triggers file open event.
 * 
 * @param
 *     void
 * @returns
 *     void
 */

static void watch_plugin_directory(void)
{
    syslog(LOG_INFO|LOG_LOCAL0,"path = %s\n",path);
    int fd, poll_num;
    int *wd;
    nfds_t nfds;
    struct pollfd fds[1];

    /* Create the file descriptor for accessing the inotify API */
    fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0)
    {
        perror("inotify_init1 ");
    }

    /* Allocate memory for watch descriptors */
    wd = calloc(1, sizeof(int));
    if (wd == NULL) {
        perror("calloc");
    }

    /* Mark directories for events
       - file was opened
       - file was closed */

    *wd = inotify_add_watch(fd, path, IN_OPEN);
    if (*wd < 0) {
        perror("inotify_add_watch");
    }

    /* Prepare for polling */
    nfds = 1;

    /* Inotify input */
    fds[0].fd = fd;
    fds[0].events = POLLIN;

    /* Wait for events and/or terminal input */
    while (1)
    {
        poll_num = poll(fds, nfds, -1);

        if (poll_num == -1)
        {
            if (errno == EINTR)
                continue;

            perror("poll");
        }
        if (poll_num > 0)
        {
            if (fds[0].revents & POLLIN)
            {
                /* Inotify events are available */
                handle_file_event(fd);
            }
        }
        /* check after 3 second for file changes*/
        sleep(3);
    }
}

/** checks for .so files in the folder
 * /opt/secmon/plugins and loads if any .so
 * are present and listens for file creation 
 * events(.so files) on the same folder.
 * 
 * @param 
 *     void
 * @returns
 *     void
 */

static void plugin_loader(void)
{
    int len;
    DIR *d;
    struct dirent *dir;
    d = opendir(path);
    if (d)
    {
        while ((dir = readdir(d)) != NULL)
        {
            len = strlen(dir->d_name);
            if(len > FILE_EXTN_LEN)
            {
                /* load only .so files */
                if((strcmp(&dir->d_name[len - FILE_EXTN_LEN],".so")) == 0)
                {
                    load_plugin(dir->d_name);
                }
            }
        }
        closedir(d);
    }

    watch_plugin_directory();
}

/** callback function for handling file creation 
 * event in /opt/secmon/plugins folder
 * invokes load_plugin function if the file created 
 * has .so extension
 * 
 * @param 
 *	fd - file descriptor of the directory
 * @returns
 *	void
 */

static void handle_file_event(int fd)
{
    char buf[MAX_EVENT_LENGTH]
        __attribute__ ((aligned(__alignof__(struct inotify_event))));
    const struct inotify_event *event;
    ssize_t len;
    /* Read some events. */
    len = read(fd, buf, sizeof buf);
    if (len == -1 && errno != EAGAIN)
    {
        perror("read error\n");
    }

    /* If the nonblocking read() found no events to read, then
       it returns -1 with errno set to EAGAIN. In that case,
       we exit the loop. */

    if (len <= 0)
        return;
    /* Loop over all events in the buffer */
    event = (const struct inotify_event *) buf;

    /* Print event type */
    if (event->mask & IN_CREATE)
        syslog(LOG_INFO|LOG_LOCAL0,"IN_CREATE: ");

    /* Print the name of the file */
    if (event->len)
    {
        if((strcmp(&event->name[strlen(event->name)-3],".so")) == 0)
        {
            syslog(LOG_INFO|LOG_LOCAL0,"added dynamically\n");
            load_plugin(event->name);
        }
    }
}

/** loads the plugin into process address space
 * when some .so file is copied to the folder 
 * /opt/secmon/plugins
 * 
 * @param  
 *	file - name of the .so file to load
 * @returns 
 *	void
 */

static void load_plugin(const char *file)
{
    int conf_key=0;
    int data_key=0;
    char *error;
    int ret=0;

    syslog(LOG_INFO|LOG_LOCAL0,"loading plugin...%s\n", file);

    do {
        handle = dlopen(file,RTLD_LAZY | RTLD_NOLOAD);

        if(!handle)
        {
            if(dlerror() == NULL)
            {
                syslog(LOG_INFO|LOG_LOCAL0,"library is not loaded. Loading it...\n");

                handle = dlopen(file,RTLD_LAZY);
                if(!handle)
                {
                    syslog(LOG_CRIT|LOG_LOCAL0,"dlopen error %s",dlerror());
                    break;
                }

                syslog(LOG_INFO|LOG_LOCAL0,"loading init symbol\n");

                /* call init function*/
                init = dlsym(handle,"init");
                if ((error = dlerror()) != NULL)  {
                    syslog(LOG_INFO|LOG_LOCAL0,"error calling init function...\n");
                }


                syslog(LOG_INFO|LOG_LOCAL0,"calling init function...\n");
                ret = (*init)();
                if(ret == 0)
                {
                    /* call receive_data function*/
                    syslog(LOG_INFO|LOG_LOCAL0,"calling receive_data function...\n");

                    receive_data = dlsym(handle,"receive_data");
                    if ((error = dlerror()) != NULL)  {
                        syslog(LOG_CRIT|LOG_LOCAL0,"error calling receive_data function...\n");
                    }
                    (*receive_data)(data_key);

                    /* to ensure that all the plugin threads are started
                     * before calling further functions */
                    sleep(1);

                    /* call config function*/
                    syslog(LOG_INFO|LOG_LOCAL0,"calling config function...\n");
                    config = dlsym(handle,"config");
                    if ((error = dlerror()) != NULL)  {
                        syslog(LOG_CRIT|LOG_LOCAL0,"error calling config function...\n");
                    }
                    (*config)(conf_key);
                    /* load send_packet symbol*/
                    syslog(LOG_INFO|LOG_LOCAL0,"calling send_packet function...\n");
                    send_packet[plugins] = dlsym(handle,"receive_from_secmon");
                    if ((error = dlerror()) != NULL)  {
                        syslog(LOG_CRIT|LOG_LOCAL0,"error calling send_packet function of plugin %d...\n",plugins);
                    }
                    plugins++;
                }

            }
            else
            {
                syslog(LOG_CRIT|LOG_LOCAL0,"dlopen error:\n");
            }
            dlerror();
        }
        else
        {
            syslog(LOG_INFO|LOG_LOCAL0,"library already loaded\n");
        }
    }while(0);
}

/** calls receiver_thread function on specified core 
 * 
 * @param dummy 
 *     unused argument
 * @return 
 *     SUCCESS 
 */

static int packet_receiver_lcore(__attribute__((unused)) void *dummy)
{
    syslog(LOG_INFO|LOG_LOCAL0,"packet receiver lcore Id %d\n",rte_gettid());
    receiver_thread();
    return SUCCESS;
}


/** display usage of program
 * 
 * @param prgname
 *     program name
 * @return 
 *     void
 */

static void l2fwd_usage(const char *prgname)
{
    syslog(LOG_INFO|LOG_LOCAL0, "%s [EAL options] -- -p PORTMASK [-q NQ]\n"
            "  -p PORTMASK: hexadecimal bitmask of ports to configure\n"
            "  -q NQ: number of queue (=ports) per lcore (default is 1)\n"
            "  -T PERIOD: statistics will be refreshed each PERIOD seconds (0 to disable, 10 default, 86400 maximum)\n",
            prgname);
}

/** parses the hexadecimal portmask and converts it into decimal value.
 * 
 * @param portmask
 *     portmask in hexadecimal format
 * @return
 *     int - portmask in decimal format
 */

static int l2fwd_parse_portmask(const char *portmask)
{
    char *end = NULL;
    unsigned long pm;

    /* parse hexadecimal string */
    pm = strtoul(portmask, &end, 16);
    if ((portmask[0] == '\0') || (end == NULL) || (*end != '\0'))
        return INVALID;

    if (pm == 0)
        return INVALID;

    return pm;
}

/** parses the number of rx queues argument given and validates it
 * 
 * @param q_arg 
 *     number of rx queues
 * @return 
 *     number of rx queues in decimal format if validation succeeds.
 *     -1 if validation fails.
 */

static unsigned int l2fwd_parse_nqueue(const char *q_arg)
{
    char *end = NULL;
    unsigned long n;

    /* parse hexadecimal string */
    n = strtoul(q_arg, &end, 10);
    if ((q_arg[0] == '\0') || (end == NULL) || (*end != '\0'))
        return INVALID;
    if (n == 0)
        return INVALID;
    if (n >= MAX_RX_QUEUE_PER_LCORE)
        return INVALID;

    return n;
}

/** parses the timer period, validates and converts it from 
 * string format to decimal format. 
 * 
 * @param q_arg
 *     timer period
 * @return
 *     timer period in decimal format if validation succeeds.
 *     -1 if validation fails.
 */

static int l2fwd_parse_timer_period(const char *q_arg)
{
    char *end = NULL;
    int n;

    /* parse number string */
    n = strtol(q_arg, &end, 10);
    if ((q_arg[0] == '\0') || (end == NULL) || (*end != '\0'))
        return FAILURE;
    if (n >= MAX_TIMER_PERIOD)
        return FAILURE;

    return n;
}

/** parse the argument given in the command line of the application 
 * 
 * @param argc
 *     number of arguments given
 * @param argv
 *     pointer to array of arguments
 * @return 
 *     number of arguments parsed successfully.
 *     -1 in case of any invalid arguments.
 */

static int l2fwd_parse_args(int argc, char **argv)
{
    int opt, ret;
    char **argvopt;
    int option_index;
    char *prgname = argv[0];
    static struct option lgopts[] = {
        {NULL, 0, 0, 0}
    };

    argvopt = argv;

    while ((opt = getopt_long(argc, argvopt, "p:q:T:",
                    lgopts, &option_index)) != EOF) {

        switch (opt) {
            /* portmask */
            case 'p':
                l2fwd_enabled_port_mask = l2fwd_parse_portmask(optarg);
                if (l2fwd_enabled_port_mask == INVALID) {
                    syslog(LOG_INFO|LOG_LOCAL0, "invalid portmask\n");
                    l2fwd_usage(prgname);
                    return FAILURE;
                }
                break;

                /* nqueue */
            case 'q':
                l2fwd_rx_queue_per_lcore = l2fwd_parse_nqueue(optarg);
                if (l2fwd_rx_queue_per_lcore == INVALID) {
                    syslog(LOG_INFO|LOG_LOCAL0, "invalid queue number\n");
                    l2fwd_usage(prgname);
                    return FAILURE;
                }
                break;

                /* timer period */
            case 'T':
                timer_period = l2fwd_parse_timer_period(optarg) * 1000 * TIMER_MILLISECOND;
                if (timer_period < 0) {
                    syslog(LOG_INFO|LOG_LOCAL0, "invalid timer period\n");
                    l2fwd_usage(prgname);
                    return FAILURE;
                }
                break;

                /* long options */
            case 0:
                l2fwd_usage(prgname);
                return FAILURE;

            default:
                l2fwd_usage(prgname);
                return FAILURE;
        }
    }

    if (optind >= 0)
        argv[optind-1] = prgname;

    ret = optind-1;
    optind = 0; /* reset getopt lib */
    return ret;
}

/** Check the link status of all ports in up to 9s, and print them finally 
 *
 * @param port_num
 *     number of ports to check
 * @param port_mask
 *     hexadecimal port mask
 * @return 
 *     void
 */
static void check_all_ports_link_status(unsigned char port_num, unsigned int port_mask)
{
    uint8_t portid, count, all_ports_up, print_flag = 0;
    struct rte_eth_link link;

    syslog(LOG_INFO|LOG_LOCAL0,"\nChecking link status");
    fflush(stdout);
    for (count = 0; count <= MAX_CHECK_TIME; count++) {
        all_ports_up = 1;
        for (portid = 0; portid < port_num; portid++) {
            if ((port_mask & (1 << portid)) == 0)
                continue;
            memset(&link, 0, sizeof(link));
            rte_eth_link_get_nowait(portid, &link);
            /* print link status if flag set */
            if (print_flag == 1) {
                if (link.link_status)
                    syslog(LOG_INFO|LOG_LOCAL0, "Port %d Link Up - speed %u "
                            "Mbps - %s\n", (uint8_t)portid,
                            (unsigned)link.link_speed,
                            (link.link_duplex == ETH_LINK_FULL_DUPLEX) ?
                            ("full-duplex") : ("half-duplex\n"));
                else
                    syslog(LOG_INFO|LOG_LOCAL0, "Port %d Link Down\n",
                            (uint8_t)portid);
                continue;
            }
            /* clear all_ports_up flag if any link down */
            if (link.link_status == 0) {
                all_ports_up = 0;
                break;
            }
        }
        /* after finally printing all link status, get out */
        if (print_flag == 1)
            break;

        if (all_ports_up == 0) {
            syslog(LOG_INFO|LOG_LOCAL0, ".");
            fflush(stdout);
            rte_delay_ms(CHECK_INTERVAL);
        }

        /* set the print_flag if all ports up or timeout */
        if (all_ports_up == 1 || count == (MAX_CHECK_TIME - 1)) {
            print_flag = 1;
            syslog(LOG_INFO|LOG_LOCAL0,"done\n");
        }
    }
}

/** Entry function for the SecMonAgent dpdk application.
 *
 * Parses and validates the eal (environment abstraction layer) arguments.
 * Initializes the ports given in portmask
 * launches the receiver_thread() function on lcore 1.
 * listen for plugins (.so files) in /opt/secmon/plugins
 *
 * @param argc 
 *     number of command line arguments
 * @param argv
 *     pointer to array of arguments
 * @return
 *     it will never return
 */

int main(int argc, char **argv)
{
    struct lcore_queue_conf *qconf;
    int ret;
    uint8_t nb_ports;
    uint8_t nb_ports_available;
    uint8_t portid=0, lcoreid;
    unsigned lcore_id, rx_lcore_id;

    /*open log */
    openlog("NFV", LOG_PID|LOG_CONS, LOG_LOCAL0);
    syslog(LOG_INFO|LOG_LOCAL0,"in secmonagent\n");

    /* init EAL (Environment Abstraction layer) */
    ret = rte_eal_init(argc, argv);
    if (ret < 0)
        rte_exit(EXIT_FAILURE, "Invalid EAL arguments\n");
    argc -= ret;
    argv += ret;

    /* return id of execution unit in which we are running on */
    lcoreid = rte_lcore_id();

    /* parse application arguments (after the EAL ones) */
    ret = l2fwd_parse_args(argc, argv);
    if (ret < 0)
        rte_exit(EXIT_FAILURE, "Invalid L2FWD arguments\n");


    /* create the mbuf pool */
    l2fwd_pktmbuf_pool =
        rte_mempool_create("mbuf_pool", NB_MBUF,
                MBUF_SIZE, MAX_PKT_BURST,
                sizeof(struct rte_pktmbuf_pool_private),
                rte_pktmbuf_pool_init, NULL,
                rte_pktmbuf_init, NULL,
                rte_socket_id(), 0);
    if (l2fwd_pktmbuf_pool == NULL)
        rte_exit(EXIT_FAILURE, "Cannot init mbuf pool\n");

    nb_ports = rte_eth_dev_count();
    syslog(LOG_INFO|LOG_LOCAL0, "*** DPDK Controlled Ports = %d, Port_mask=%d\n",nb_ports,l2fwd_enabled_port_mask);
    if (nb_ports == 0)
        rte_exit(EXIT_FAILURE, "No Ethernet ports - bye\n");

    if (nb_ports > RTE_MAX_ETHPORTS)
        nb_ports = RTE_MAX_ETHPORTS;


    rx_lcore_id = 1;
    qconf = NULL;

    /* get the lcore_id for this port */
    while (rte_lcore_is_enabled(rx_lcore_id) == 0 ||
            lcore_queue_conf[1].n_rx_port == l2fwd_rx_queue_per_lcore) 
    {

        if (rx_lcore_id >= RTE_MAX_LCORE)
            rte_exit(EXIT_FAILURE, "Not enough cores\n");
    }

    if (qconf != &lcore_queue_conf[rx_lcore_id])
    {    
        qconf = &lcore_queue_conf[rx_lcore_id];
    }

    qconf->rx_port_list[qconf->n_rx_port] = 0;
    qconf->n_rx_port++;
    syslog(LOG_INFO|LOG_LOCAL0, "Lcore %u: RX port %u\n", lcoreid,portid);


    nb_ports_available = nb_ports;

    /* Initialize each port */
    for (portid = 0; portid < nb_ports; portid++) {
        /* skip ports that are not enabled */
        if ((l2fwd_enabled_port_mask & (1 << portid)) == 0) {
            syslog(LOG_INFO|LOG_LOCAL0, "Skipping disabled port %u\n", (unsigned) portid);
            nb_ports_available--;
            continue;
        }
        /* init port */
        syslog(LOG_INFO|LOG_LOCAL0, "Initializing port %u... ", (unsigned) portid);
        fflush(stdout);

        ret = rte_eth_dev_configure(portid, 1, 1, &port_conf);
        if (ret < 0)
            rte_exit(EXIT_FAILURE, "Cannot configure device: err=%d, port=%u\n",
                    ret, (unsigned) portid);

        rte_eth_macaddr_get(portid,&l2fwd_ports_eth_addr[portid]);

        /* init one RX queue */
        fflush(stdout);
        unsigned int k;
        for(k=0; k < l2fwd_rx_queue_per_lcore;k++)
        {
            ret = rte_eth_rx_queue_setup(portid, k, nb_rxd,
                    rte_eth_dev_socket_id(portid),
                    NULL,
                    l2fwd_pktmbuf_pool);
            if (ret < 0)
                rte_exit(EXIT_FAILURE, "rte_eth_rx_queue_setup:err=%d, port=%u\n",
                        ret, (unsigned) portid);
        }

        /* init one TX queue on each port */
        fflush(stdout);
        ret = rte_eth_tx_queue_setup(portid,0,nb_txd,rte_eth_dev_socket_id(portid),NULL);
        if(ret < 0)
        {
            rte_exit(EXIT_FAILURE,"rte_eth_rx_queue_setup:err=%d, portid=%u\n",ret ,(unsigned) portid);
        }
        /* Start device */
        ret = rte_eth_dev_start(portid);
        if (ret < 0)
            rte_exit(EXIT_FAILURE, "rte_eth_dev_start:err=%d, port=%u\n",
                    ret, (unsigned) portid);

        syslog(LOG_INFO|LOG_LOCAL0, "done: \n");

        rte_eth_promiscuous_enable(0);

        syslog(LOG_INFO|LOG_LOCAL0, "Port %u, MAC address: %02X:%02X:%02X:%02X:%02X:%02X\n\n",
                (unsigned) portid,
                l2fwd_ports_eth_addr[portid].addr_bytes[0],
                l2fwd_ports_eth_addr[portid].addr_bytes[1],
                l2fwd_ports_eth_addr[portid].addr_bytes[2],
                l2fwd_ports_eth_addr[portid].addr_bytes[3],
                l2fwd_ports_eth_addr[portid].addr_bytes[4],
                l2fwd_ports_eth_addr[portid].addr_bytes[5]);

        /* initialize port stats */
        memset(&port_statistics, 0, sizeof(port_statistics));
    }

    check_all_ports_link_status(nb_ports, l2fwd_enabled_port_mask);

    /* launch per-lcore init on every lcore */
    if(rte_eal_get_lcore_state(0) != 0)
    {
        syslog(LOG_INFO|LOG_LOCAL0, "lcore 0 is busy\n");
        closelog();
        return FAILURE;
    }

    /* launch function on another lcore */
    rte_eal_remote_launch(packet_receiver_lcore,NULL,DPDK_CORE_ID);

    /* check for plugins in plugins directory and load them if present */
    plugin_loader();

    syslog(LOG_INFO|LOG_LOCAL0,"after configuration thread\n");
    RTE_LCORE_FOREACH_SLAVE(lcore_id) 
    {
        if(rte_eal_wait_lcore(lcore_id) < 0)
        {
            closelog();
            return FAILURE;
        }
    }

    closelog();
    return SUCCESS;
}


/** parses the data packet to strip gtp header
 * 
 * @param secmon_pkt 
 * 		address of pointer to the packet 
 * @return  
 *      stripped length
 */
void strip_gtp_header(struct rte_mbuf *m)
{
    struct ether_header *eth_hdr;
    struct ipv4_header *ipv4_hdr;
    uint16_t etherType;
    char *pkt = (char *)rte_pktmbuf_mtod(m,char *);
    eth_hdr = (struct ether_header *) pkt;
    struct udp_header *udphdr;

    etherType = htons(eth_hdr->ether_type);
    if(likely(etherType == VLAN))
    {
        /* VLAN Segment size in ethernet header is 4 bytes */
        pkt += VLAN_HEADER_LEN;  

        /* GTP header check is performed initially for performance 
         * improvement. 
         * later ipv4 and udp header checks are performed for confirmation
         * that the packet actually contains GTP header
         * */
        udphdr = (struct udp_header *)(pkt + IPV4_L4_HDR_OFFSET);
        if((ntohs(udphdr->dst_port)) == PROTO_GTP)
        {
            /* recast eth_hdr structure to point 
             * etherType to actual etherType */
            eth_hdr = (struct ether_header *) pkt;
            etherType = htons(eth_hdr->ether_type);

            if(likely(etherType == IPV4_PACKET))
            {
                ipv4_hdr = (struct ipv4_header *) (pkt + MAC_HEADER_LEN);
                if(likely(ipv4_hdr->next_proto_id == IPPROTO_UDP))
                {
                    shift_mac(pkt-VLAN_HEADER_LEN,MAC_VLAN_HDR);
                    rte_pktmbuf_adj(m,MAC_SHIFT_LEN);
                }
            }
        }
    }
    else
    {
        /* non vlan tagged packet handling. 
         * in case of taas ,  this case is most unlikely 
         */
    }
}
