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

import configparser

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set IPsecEnforcer Config"

    def add_arguments(self, parser):
        parser.add_argument('vpnendpoint_name', type=str)
        parser.add_argument('vpnendpoint_type', type=str)
        parser.add_argument('ipsec_tunnel_interface', type=str)
        parser.add_argument('ipsec_ems_interface', type=str)
        parser.add_argument('ipsec_ems_ip', type=str)

    def handle(self, *args, **options):
        ipsecenforcer_config_file = 'registration/ipsecenforcer.ini'
        config = configparser.ConfigParser()
        config.read(ipsecenforcer_config_file)
        config['ENDPOINT']['NAME_AND_TYPE'] = ('(' +
                                               options[
                                                   'vpnendpoint_name'] + ', ' +
                                               options['vpnendpoint_type'] +
                                               ')')
        config['INTERFACE']['IPSEC_TUNNEL_INTERFACE'] = \
            options['ipsec_tunnel_interface']
        config['INTERFACE']['IPSEC_EMS_INTERFACE'] = \
            options['ipsec_ems_interface']
        config['IPSEC_EMS_CONTROLLER']['IP_ADDRESS_WITH_PORT'] =  \
            options['ipsec_ems_ip']
        config['IPSEC_EMS']['IP_ADDRESS_WITH_PORT'] = \
            options['ipsec_ems_ip']

        with open(ipsecenforcer_config_file, 'w') as config_file:
            config.write(config_file)
