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

"""IPsec Enforcer Health Check by sending a heartbeat message at
regular intervals.

This heartbeat message is a HTTP GET request. When, the IPsec Enforcer
responds with a HTTP 200 (OK), it means the IPsec Enforcer is
reachable.

The IPsec Enforcer exposes a REST endpoint for health check.

This health check module runs as a independent background process. This
process is started by a custom command. The command name is
'healthcheck'. This custom command is defined in 'management' module.

To start the process, run the below command:
$ python manage.py healthcheck

This process is started in the IPsec EMS startup script.
"""

import httplib as http_status_code
import logging
from multiprocessing import Pool
from time import sleep

import requests
from django.utils.translation import ugettext as _

from services.api import storage
from services.api.serializers.serializers_enforcer_registration import (
    IPsecEnforcerRegistration
)
from services.api.serializers.vpn_choices import RESOURCE_TO_RELATION_MAP
from services.ipsecenforcer.notification_ipc_client_listener import (
    IPsecEnforcerNotification
)
from services.ipsecenforcer.register_deregister import (
    HeartbeatMissOfIPsecEnforcer, IPsecEnforcerInfo
)
from services.ipsecenforcer.send_notification import IPsecEnforcerNotify

LOG = logging.getLogger(__name__)

# The health check process awakes after the duration to send the heartbeat
# message to all the IPsec Enforcers.
HEALTH_CHECK_DURATION = 60  # in seconds

# Number of count before de-registering(deleting) the IPsecEnforcer
# record(and related info.)
BACKOFF_COUNT = 10

# REST endpoint provided by IPsec Enforcer just for health checking
healthcheck_rest_endpoint = 'heartbeat'


class IPsecEnforcerHealthCheck(object):
    """Health check for IPsecEnforcer

    Send a heartbeat message at regular interval to every registered
    IPsecEnforcer to check whether the IPsecEnforcer is
    alive(reachable).

    The IPsecEnforcer could become unreachable if the IPsecEnforcer
    service on workload(VM) crashes. Or the workload(VM) shuts down,
    reboots or becomes unreachable.
    """

    @staticmethod
    def start():
        """Start the IPsecEnforcer Health check

        The Health check process periodically awakes and checks the
        health of IPsecEnforcer(s)
        """
        LOG.info(_("Starting Health Check Process"))
        p = Pool(2)
        while True:
            relation = RESOURCE_TO_RELATION_MAP['IPsecEnforcerRegistration']
            ipsecenforcers = storage.plugin.get_records(relation)

            # Prepare a list of IPsecEnforcer 'fqdn' & 'id' tuple
            fqdn_enforcer_list = [(ipsecenforcer['fqdn'], ipsecenforcer['id'])
                                  for ipsecenforcer in ipsecenforcers]

            # If the list is not empty
            if fqdn_enforcer_list:
                # Check the health all the IPsecEnforcer
                p.map(check_ipsecenforcer_health, fqdn_enforcer_list)

            # Wait before again checking the IPsecEnforcer(s) health
            LOG.debug(_("Health Check Process sleeping"))
            sleep(HEALTH_CHECK_DURATION)
            LOG.debug(_("Health Check Process awakened"))


def check_ipsecenforcer_health(fqdn_enforcer):
    """Check health of IPsecEnforcer by sending a HTTP request.

    Args:
        fqdn_enforcer (tuple): IPsecEnforcer's FQDN and id
    """

    fqdn = fqdn_enforcer[0]
    ipsecenforcer_id = fqdn_enforcer[1]
    response = None
    try:
        response = requests.get(IPsecEnforcerNotify.prepare_url(
                fqdn,
                ipsecenforcer_id,
                url_endpoint=healthcheck_rest_endpoint))
        LOG.debug(_("Healthcheck success for IPsecEnforcer id %s "
                    "with FQDN %s" % (ipsecenforcer_id, fqdn)))
    except requests.exceptions.ConnectionError:
            pass

    #
    # Health Check Failure
    #
    if (response is None) or (response.status_code != http_status_code.OK):
        count = HeartbeatMissOfIPsecEnforcer().get_heartbeat_miss_count(
                        ipsecenforcer_id,
                        fqdn)

        # Health Check failure for the first time
        if count == 0:
            LOG.debug(_("First Heartbeat Miss for IPsecEnforcer id %s "
                        "with FQDN %s" % (ipsecenforcer_id, fqdn)))
            # Initialize with count 1
            HeartbeatMissOfIPsecEnforcer().put_heartbeat_miss_count(
                    ipsecenforcer_id,
                    fqdn,
                    1)

        # Increment the count every time the health check fails
        elif count < BACKOFF_COUNT:
            LOG.debug(_("Heartbeat Miss count %s for IPsecEnforcer id "
                        "%s with FQDN %s" %
                        (count, ipsecenforcer_id, fqdn)))
            HeartbeatMissOfIPsecEnforcer().put_heartbeat_miss_count(
                    ipsecenforcer_id,
                    fqdn,
                    count + 1)

        # Delete the IPsecEnforcer (and related info.) if the count
        # becomes equal to BACKOFF_COUNT
        elif count == BACKOFF_COUNT:
            LOG.debug(_("Heartbeat Miss count equals to backoff count "
                        "%s for IPsecEnforcer id %s with FQDN %s" %
                        (count, ipsecenforcer_id, fqdn)))

            # Before De-Registration(deletion), fetch all the
            # VPNEndpoint(s) associated with IPsecEnforcer.
            mapping_records = (
                IPsecEnforcerInfo.get_ipsecenforcer_to_vpnendpoint_map(
                    ipsecenforcer_id)
            )

            # De-Register the IPsecEnforcer
            ipsecenforcer_record = IPsecEnforcerRegistration.get(
                    id=ipsecenforcer_id)
            IPsecEnforcerInfo().deregister_ipsecenforcer(
                    ipsecenforcer_record)

            # Notify the peer IPsecEnforcer(s)
            IPsecEnforcerNotification.client_ipsecenforcer_deregister(
                ipsecenforcer_id,
                mapping_records)

    #
    # Health Check Success
    #
    # Initialize or Reset the heartbeat count to 0 if the
    # IPsecEnforcer is reachable
    if (response is not None) and (response.status_code == http_status_code.OK):
        HeartbeatMissOfIPsecEnforcer().put_heartbeat_miss_count(
                ipsecenforcer_id,
                fqdn,
                0)
        LOG.debug(_("Heartbeat miss count reset for IPsecEnforcer id "
                    "%s with FQDN %s" % (ipsecenforcer_id, fqdn)))