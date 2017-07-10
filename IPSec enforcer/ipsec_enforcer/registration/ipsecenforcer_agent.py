from multiprocessing.connection import Listener
import json
import requests
import socket
from collections import deque

import time
from ipsecenforcer_utils import get_ipsec_enforcer_info, mac_for_ip, \
    get_ipsec_tunnel_and_ems_ip
from prepare_vpn_configurations import install_configurations

IPSEC_ENFORCER_ID = None
IPSEC_ENFORCER_FQDN = None
IPSEC_EMS_CONTROLLER_FQDN_DEQUE, ENDPOINT_NAME_TYPE = get_ipsec_enforcer_info()

IPSEC_EMS_FQDN_DEQUE = deque()
IPSEC_EMS_REGISTRATION = 'v1/main/ipsecvpn/ipsecenforcerregistrations'
IPSEC_EMS_POLICY_CONFIG = 'v1/main/ipsecvpn/ipsecenforcerregistrations'

CONFIG_VERSION = 0


class IPsecEnforcer(object):
    def __init__(self):
        self.endpoint_name = []
        self.endpoint_type = []
        for endpoint in ENDPOINT_NAME_TYPE:
            endpoint = endpoint[1:-1].split(',')
            self.endpoint_name.append(endpoint[0].strip())
            self.endpoint_type.append(endpoint[1].strip())
        self.description = socket.gethostname()
        self.instance_id = ''  # TODO: Add AWS or OS instance-id
        self.fqdn_tunnel, self.fqdn = get_ipsec_tunnel_and_ems_ip()
        self.macaddress = mac_for_ip(self.fqdn)
        global IPSEC_ENFORCER_FQDN_TUNNEL
        IPSEC_ENFORCER_FQDN_TUNNEL = self.fqdn_tunnel


# while True:
#         ipsec_ems_list_uri = ('http://' + EMS_CONTROLLER_FQDN_DEQUE[0] + '/' +
#                               EMS_CONTROLLER_FQDN_DEQUE)
#         r = requests.get(ipsec_ems_list_uri)
#         if r.status_code == requests.codes.ok:
#             IPSEC_EMS_FQDN_DEQUE = deque(r.json())
#             break;
#         else:
#             EMS_CONTROLLER_FQDN_DEQUE.rotate(-1)
#             time.sleep(30)


class IPsecEnforcerAgent(object):

    @staticmethod
    def start():
        IPSEC_EMS_FQDN_DEQUE = IPSEC_EMS_CONTROLLER_FQDN_DEQUE
        ipsec_enforcer = IPsecEnforcer()
        ipsec_enforcer_socket = Listener(('localhost', 8081))
        while True:
            registration_uri = ('http://' + IPSEC_EMS_FQDN_DEQUE[0] + '/' +
                                IPSEC_EMS_REGISTRATION + '/')
            data = json.dumps(ipsec_enforcer.__dict__)
            response = requests.post(registration_uri, data=data)
            if response.status_code == requests.codes.created:
                IPSEC_ENFORCER_ID = response.json()['id']
                break
            else:
                IPSEC_EMS_FQDN_DEQUE.rotate(-1)
                time.sleep(30)

        while True:
            registration_uri = ('http://' + IPSEC_EMS_FQDN_DEQUE[0] + '/' +
                                IPSEC_EMS_POLICY_CONFIG + '/' +
                                IPSEC_ENFORCER_ID + '/')
            response = requests.get(registration_uri)

            if response.status_code == requests.codes.ok:
                response = response.json()

                if response.get('version') > CONFIG_VERSION:
                    install_configurations(response, IPSEC_ENFORCER_FQDN_TUNNEL)
            else:
                IPSEC_EMS_FQDN_DEQUE.rotate(-1)
                time.sleep(10)
            conn = ipsec_enforcer_socket.accept()
            response = None
