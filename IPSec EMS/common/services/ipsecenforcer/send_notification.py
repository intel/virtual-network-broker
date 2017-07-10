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

"""HTTP Notification to IPsecEnforcer"""

import httplib as http_status_code
import logging

import requests

from django.utils.translation import ugettext as _

from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo

LOG = logging.getLogger(__name__)

IPSECENFORCER_PORT = 8001


class IPsecEnforcerNotify(object):
    @classmethod
    def vpnbind_endpoints_update(cls, vpnendpoint_id, peer_vpnendpoint_id):
        """Notify all the IPsecEnforcer(s) corresponding to both
        VPNEndpoint and Peer VPNEndpoint of the VPNBind record

        Args:
            vpnendpoint_id (str): id of VPNEndpoint record
            peer_vpnendpoint_id (str): id of Peer VPNEndpoint record
        """
        LOG.debug(_("Notify VPNEndpoint %s of VPNBIND") % vpnendpoint_id)
        cls.notify_ipsecenforcers_of_vpnendpoint(vpnendpoint_id)

        LOG.debug(_("Notify Peer-VPNEndpoint %s of VPNBIND") %
                  peer_vpnendpoint_id)
        cls.notify_ipsecenforcers_of_vpnendpoint(peer_vpnendpoint_id)

    @classmethod
    def notify_ipsecenforcers_of_vpnendpoint(cls, vpnendpoint_id):
        """Notify all the IPsecEnforcer(s) of the VPNEndpoint record

        Args:
            vpnendpoint_id (str): ID of VPNEndpoint record
        """
        # Fetch all the  IPsecEnforcers that belong to VPNEndpoint record
        ipsecenforcers_fqdn_id = (
            IPsecEnforcerInfo().get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(
                    vpnendpoint_id)
        )

        # Remove duplicates to make sure that each IPsecEnforcer will receive a
        # single notification
        ipsecenforcers_fqdn_id = {v['fqdn']: v for v in
                                  ipsecenforcers_fqdn_id}.values()
        map(cls.notify_ipsecenforcers, ipsecenforcers_fqdn_id)

    @classmethod
    def notify_ipsecenforcers(cls, ipsecenforcer_fqdn_id):
        """Notify all the IPsecEnforcer(s)

        Args:
            ipsecenforcer_fqdn_id (dict): IPsecEnforcer (FQDN & id)
        """
        ipsecenforcer_fqdn = ipsecenforcer_fqdn_id['fqdn']
        ipsecenforcer_id = ipsecenforcer_fqdn_id['ipsecenforcer_id']

        try:
            # Send a HTTP GET request to each IPsecEnforcer
            response = requests.get(cls.prepare_url(
                       ipsecenforcer_fqdn,
                       ipsecenforcer_id
            ))
            if response.status_code == http_status_code.OK:
                LOG.info(_("Successfully notified %s(FQDN: %s)" %
                        (ipsecenforcer_id, ipsecenforcer_fqdn)))
            else:
                LOG.info(_("Failed to notify %s(FQDN: %s)" %
                        (ipsecenforcer_id, ipsecenforcer_fqdn)))

        except requests.exceptions.ConnectionError:
            LOG.info(_("Failed to notify %s(FQDN: %s)" %
                           (ipsecenforcer_id, ipsecenforcer_fqdn)))
            pass

    @classmethod
    def prepare_url(cls, fqdn, ipsecenforcer_id, url_endpoint='configupdate'):
        """Prepare the URL of the IPsecEnforcer for a particular
        endpoint

        'configupdate' is a REST endpoint for config
            registration/update/deletion on IPsecEnforcer webservice.

        'healthcheck' is a REST endpoint for heartbeat message
            (or healthcheck) on IPsecEnforcer webservice.

        Args:
            fqdn (str): FQDN of IPsecEnforcer
            ipsecenforcer_id (str): ID of IPsecEnforcer
            url_endpoint (str): name of endpoint
                (e.g. configupdate, healthcheck, etc.)

        Returns:
            str: Complete endpoint URL for IPsecEnforcer health check
        """
        url = '{0}://{1}:{2}/{3}/{4}/{5}/{6}/{7}/'.format('http',
                                                          fqdn,
                                                          IPSECENFORCER_PORT,
                                                          'v1',
                                                          'main',
                                                          'ipsecvpn',
                                                          url_endpoint,
                                                          ipsecenforcer_id)
        LOG.debug(_("Prepared URL %s" % url))
        return url
