# **SECMON SETUP STEPS**
======================================================================================================================

## ENVIRONMENT
===============

Operating System: Ubuntu 14.04

DPDK version: 2.0.0

CPU Cores required by Secmon: 2

## STEPS TO INSTALL AND RUN SECMON
====================================

1.  Install the JSON and curl libraries:
    `$ apt-get install curl libcurl3 libcurl3-dev php5-curl
    libcurl4-openssl-dev`
    `$ apt-get install libjson0 libjson0-dev build-essential make`

2.  Installing DPDK in SecMon Machine:
    1.  Download DPDK 2.0.0 source from Intel DPDK web site. And
        extract the content of the archive file.
        (http://dpdk.org/browse/dpdk/snapshot/dpdk-2.0.0.tar.gz)
    2.  Change to dpdk directory e.g. `$ cd /home/intel/dpdk-2.0.0/`
    3.  Run the command : `$ make config T=x86_64-native-linuxapp-gcc`
    4.  Run the command : `$ make install T=x86_64-native-linuxapp-gcc`

3.  Create Necessary directories.
    `$ mkdir –p <path where to store plugins> (ex: /opt/secmon/plugins).`
    `$ mkdir –p <path where to store configurations> (ex: /opt/secmon/plugins/config).`
    `$ mkdir –p <path where hugepages to create> (ex: /mnt/huge).`

4.  Set these Environment variables.
    `$ export RTE_SDK=<path to your dpdk installation>.`
    `$ export LD_LIBRARY_PATH=<path where plugins stored> (ex: /opt/secmon/plugins).`
    `$ export CONFIG_PATH=<path to secmon configurations>
    (ex: /opt/secmon/plugins/config).`
    `$ export SECMON_DIR=<path to secmon code>
    (ex: /home/intel/secmon)`

5.  Change to secmon agent folder and run the following command
    `$ cd <path to secmon>/secmon_agent (ex: $SECMON_DIR/secmon_agent)`
    `$ make clean; make`

6.  Change to secmon plugins folders and build plugins
    1.  Raw forwarding plugin:
        `$ cd <path to secmon>/secmon_plugin/rawforward_plugin (ex: $SECMON_DIR/secmon_plugin/rawforward_plugin)`
        `$ make clean; make`

    2.  Netflow plugin:
        `$ cd <path to secmon>/secmon_plugin/netflow_plugin (ex: $SECMON_DIR/secmon_plugin/netflow_plugin)`
        `$ make clean; make`

7.  After building the plugins copy the .so files to /opt/secmon/plugins
    `$ cp <path to secmon>/secmon_plugin/rawforward_plugin/build/librawforward.so /opt/secmon/plugins`
    `$ cp <path to secmon>/secmon_plugin/netflow_plugin/build/libnetflow.so /opt/secmon/plugins`

1.  Configuration files in SecMon Machine:

| **file_name**          | **file_path**                    | **file contents** |
|------------------------|----------------------------------|-------------------|
| conf_params.cfg        | <config_dir> (ex: /opt/secmon/plugins/config)   | ethx (interface which is used by secmon) |
| EMS_config.ini         | <config_dir> (ex: /opt/secmon/plugins/config)   | [EMS Server Ip]:<ems server ip><br>[EMS Server Port]:9082<br>[scope]:<scope_name><br>|
| rawforward_server.ini  | <config_dir> (ex: /opt/secmon/plugins/config)   | [Server Ip]:<SecMon server_ip><br>[Server Port]:<server_port_1><br>   |
| netflow_server.ini     | <config_dir> (ex: /opt/secmon/plugins/config)   | [Server Ip]<SecMon server_ip><br> [Server Port]:<server_port_2><br>   |
| SecMonAgent_Config.ini | <config_dir> (ex: /opt/secmon/plugins/config)  | Eth1 (interface used by DPDK)            |
| Set_log_level.ini     |  <config_dir>(ex: /opt/secmon/plugins/config)   | 7 (any integer between 1 to 7)           |

1.  Allocate hugepages
    `$ mount -t hugetlbfs /mnt/huge`
    `$ sysctl vm.nr_hugepages=600`

2.  Binding Interface to DPDK.
    1.  `$cd <path to dpdk installation>/x86_64-native-linuxapp-gcc/kmod.`
    2.  Insert kernel module for UIO. Then run `$insmod igb_uio.ko.`
    3.  Then `$modprobe uio`.
    4.  `$cd <path to dpdk installation>/tools/ (ex: /home/intel/dpdk-2.0.0/tools)`.
    5.  Check status of the interfaces. (For example: In below
        screenshot showing that kernel has two interfaces).
        `$ ./dpdk_nic_bind.py --status`
        <img src="media/image1.PNG" width="456" height="200" />

    6.  Now bind one interface to dpdk by giving following command. (For
        example: In below screenshot showing that after this command one
        interface is assigned to dpdk and one is used by kernel).
        `$ ./dpdk_nic_bind.py –b igb_uio(module) 00:04.0(interface id)`
        ***Note**: skip the leading 0000*

        *Or*

        `$ ./dpdk_nic_bind.py - -bind=igb_uio(module) eth1(interface name)`
        ***Note**: Follow this command only when if= is not null. As you
        can see above if= is null*

        *that’s why we are using first command.*
        <img src="media/image2.PNG" width="469" height="186" />

3.  Run the secmon agent
    `$ cd <path to secmon>/secmon_agent/build`
    `$ SecMonAgent -c 0x3 -n 4 -m 512 –b 0000:00:03.0 -- -p 0x1 (if eth0 is binded to dpdk application)`
    `$ SecMonAgent -c 0x3 -n 4 -m 512 –b 0000:00:03.0 -- -p 0x3 (if eth1 is binded to dpdk application)`

    *-c: Set the hexadecimal bitmask of the cores to run on.*

    *-n: Set the number of memory channels to use.*

    *-m: Memory to allocate*

    *-b: Blacklist a PCI devise to prevent EAL from using it. Multiple
    -b options are allowed.*

    *-p: hexadecimal bitmask of the ports that are binded to dpdk.*

    ***Note**: You need to provide interface id of interface which
    secmon will use(not binded to dpdk) in blacklist command (-b)
    otherwise secmon try to initialize that interface also.*

## FREQUENTLY ASKED QUESTIONS (FAQ)
====================================

-   Problem: Minimum number of network interfaces required to
    run Secmon.

    Secmon require at least two interfaces to run. One interface is
    required by DPDK through which secmon will receive packets and
    another Interface is required by secmon to transmit the packets
    to collector. Interface binded to DPDK is not visible to kernel so
    we can’t use it to transmit packets to collector.

-   Problem: How should I check that packets are received by Secmon.

    First make sure that DPDK is not binded to any interface. Now send
    UDP packets to interface which you want to bind to DPDK. Now run
    ***tcpdump*** command and check that you are receiving packets
    or not. If you are not receiving packets than ***ping*** the
    interface to check that if it’s reachable from the machine from
    which we you are sending UDP packets. If ping is not working than
    check your network configurations.

-   Problem: How I can check that Secmon is receiving configurations
    from EMS.

    When you run Secmon and if it’s not able to receive configurations
    from EMS than it will show Error message stating ***“Error to
    fetch url”.*** You need to check if EMS machine is reachable from
    your Secmon machine through ***ping*** command. If its reachable you
    have to check if EMS is running or not.

-   Problem: EMS is reachable but Secmon is not receiving configurations
    from EMS.

    Check if any proxy is set. Run this command ***echo $http\_proxy***
    and ***echo $https\_proxy***. If this is set than unset it by
    running command **export http\_proxy=** and
    **export https\_proxy=.**

-   Problem: Not receiving any ACK packets from interface which is
    binded to DPDK.

    You will not receive any ACK packets from the interface which is
    used by DPDK.

-   Problem: ARP is not getting resolved to interface which is binded
    to DPDK.

    You can add static ARP entry to dpdk interface. First unbind the
    interface which is binded to DPDK and run **ifconfig** command and
    note down the mac address of the interface which you want to bind to
    DPDK and then go to other machine which is sending packets to DPDK
    interface and then type **arp –s &lt;ip address&gt; &lt;mac
    address&gt;**(ip address is of DPDK interface).

-   Problem: How I can verify that Secmon is running correctly.

    While traffic is running you can check that it if you are receiving
    packets on collector machine. After that you can make some changes
    in EMS GUI and press flush and then check that these configurations
    changes are seen on collector machine.


