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

from collections import deque
import configparser
import netifaces


def get_ipsec_enforcer_info():
    ipsec_enforcer_config = configparser.ConfigParser()
    ipsec_enforcer_config.read('registration/ipsecenforcer.ini')
    ems_name_type = ipsec_enforcer_config.get('ENDPOINT',
                                              'NAME_AND_TYPE').split('\n')
    ems_controller_fqdn = deque((ipsec_enforcer_config.get(
            'IPSEC_EMS_CONTROLLER',
            'IP_ADDRESS_WITH_PORT')).split('\n'))
    return ems_controller_fqdn, ems_name_type


def get_ipsec_tunnel_and_ems_ip():
    ipsec_enforcer_config = configparser.ConfigParser()
    ipsec_enforcer_config.read('registration/ipsecenforcer.ini')
    ipsec_tunnel_interface = ipsec_enforcer_config.get(
            'INTERFACE',
            'IPSEC_TUNNEL_INTERFACE')
    ipsec_tunnel_interface_ip = netifaces.ifaddresses(ipsec_tunnel_interface)[
        2][0]['addr']
    ipsec_ems_interface = ipsec_enforcer_config.get(
            'INTERFACE',
            'IPSEC_EMS_INTERFACE')
    ipsec_ems_interface_ip = netifaces.ifaddresses(ipsec_ems_interface)[
        2][0]['addr']
    return ipsec_tunnel_interface_ip, ipsec_ems_interface_ip

def mac_for_ip(ip):
    """Returns a list of MACs for interfaces that have given IP, returns None if
    not found"""
    for i in netifaces.interfaces():
        addrs = netifaces.ifaddresses(i)
        try:
            if_mac = addrs[netifaces.AF_LINK][0]['addr']
            if_ip = addrs[netifaces.AF_INET][0]['addr']
        except IndexError, KeyError:  # ignore ifaces that don't have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None

