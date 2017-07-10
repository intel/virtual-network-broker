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

import ast
import httplib as http_status_code
import logging
import pdb
import requests
import urllib2
from time import sleep

from ConfigDB.api import storage
from ConfigDB.secmon_notify.secmon_notification import SecMonUpdateNotification

from ConfigDB.api.serializers.serializers_secmondetails import SecmonDetails
import logging
import configfile
import inspect
# LOG = configfile.configlogging()

# The health check process awakes after the duration to send the heartbeat
# message to all the SecMons.
HEALTH_CHECK_DURATION = 30  # in seconds

# Number of count before de-registering(deleting) the SecMon 
# record(and related info.)
BACKOFF_COUNT = 5


class SecMonHealthCheck(object):
    """Health check for SecMonHealthCheck

    Send a heartbeat message at regular interval to every registered
    SecMon to check whether the SecMon is alive(reachable).

    The secmon could become unreachable if the secmon server
    on workload(VM) crashes. Or the workload(VM) shuts down,
    reboots or becomes unreachable.
    """

    # REST endpoint provided by SecMon just for health checking
#    rest_endpoint = 'healthcheck'

    def start(self):
        """Start the SecMon Health check

        The Health check process periodically awakes and checks the
        health of SecMon(s)

        Returns:
            None
        """
        relation = 'secmondetails'
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + 'healthcheck process started')
        while True:
            secmon_list = []
            secmon_data = storage.plugin.get_records(relation)
            # Prepare a list of secmon 'ip_address' & 'port' tuple
            if secmon_data is None:
#                return
                sleep(HEALTH_CHECK_DURATION)
                continue
            for data in secmon_data:
                print("inside for in healthcheck")
                record_dict = ast.literal_eval(data)
                secmon_list.append((str(record_dict['ip_address']),
                                    str(record_dict['port']),
                                    str(record_dict['id'])))
            # If the list is not empty
            if secmon_list:
                # Check the health all the SecMon
                self.check_secmon_health(secmon_list)

            # Wait before again checking the SecMon(s) health
            sleep(HEALTH_CHECK_DURATION)

    @classmethod
    def check_secmon_health(cls, secmon_address_list):
        """Check health of each secmon by sending a HTTP
        request.

        Args:
            secmon_address_list:

        Returns:
            None
        """
        for secmon_address in secmon_address_list:
            ip_address = secmon_address[0]
            port = secmon_address[1]
            response = None
            try:
                url = 'http://' + ip_address + ':' + port + '/'
                response = requests.get(url)
            except requests.exceptions.ConnectionError:
                pass
            #print("response:", response)
            #
            # Health Check Failure
            #
            if (response is None) or (response.status_code !=
                                      http_status_code.OK):
                count = HeartbeatMissOfSecMon().get_heartbeat_miss_count(ip_address, port)
                #print("count received:", count)
                # Health Check failure for the first time
                if count == 0:
                    # Initialize with count 1
                    HeartbeatMissOfSecMon().put_heartbeat_miss_count(
                            ip_address,
                            port,
                            1)

                # Increment the count every time the health check fails
                elif count < BACKOFF_COUNT:
                    HeartbeatMissOfSecMon().put_heartbeat_miss_count(
                            ip_address,
                            port,
                            count + 1)

                # Delete the SecMon (and related info.) if the count
                # becomes equal to BACKOFF_COUNT
                elif count == BACKOFF_COUNT:
                    # De-register the SecMon and delete the
                    # HeartbeatMissOfSecMon record
                    HeartbeatMissOfSecMon().delete_heartbeat_miss_count(
                            ip_address, port)
                    HeartbeatMissOfSecMon().deregister_secmon(secmon_address[2])
            #
            # Health Check Success
            #
            # Initialize or Reset the heartbeat count to 0 if the
            # SecMon is reachable
            if (response is not None) and (response.status_code ==
                                           http_status_code.OK):
                HeartbeatMissOfSecMon().put_heartbeat_miss_count(
                        ip_address,
                        port,
                        0)


class HeartbeatMissOfSecMon(object):
    """Store the Heartbeat miss count for a SecMon"""

    relation = 'heartbeat_miss_secmon'

    @classmethod
    def put_heartbeat_miss_count(cls, ip_address, port, count):
        """Store the Heartbeat record for SecMon

        Args:
            ip_address (str): IP_ADDRESS of SecMon
            port: Port of secmon plugin
            count (int): Heartbeat count

        Returns:
            None
        """
        key = cls.relation + '/' + ip_address + '/' + port
        #print("put key:", key)
        value = str(count)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' heartbeat miss count:' + value + ' set for key:' + key)
        storage.plugin.put_kv(key, value)
        count = storage.plugin.get_kv(key)

    @classmethod
    def get_heartbeat_miss_count(cls, ip_address, port):
        """Fetch the Heartbeat count for SecMon

        Args:
            ip_address (str): IP_ADDRESS of SecMon
            port: Port of secmon plugin

        Returns:
            int: Heartbeat Count of SecMon
        """
        key = cls.relation + '/' + ip_address + '/' + port
        #print("get key:", key)
        # Fetch the Heartbeat Backoff Count
        count = storage.plugin.get_kv(key)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' received heartbeat miss count for key ' + key + ' is ' + count)
        if count is None:
            return 0

        return int(count)

    @classmethod
    def delete_heartbeat_miss_count(cls, ip_address, port):
        """Delete the Heartbeat record for SecMon

        Args:
            ip_address (str): IP_ADDRESS of SecMon
            port: Port of secmon plugin

        Returns:
            None
        """
        key = cls.relation + '/' + ip_address + '/' + port
        storage.plugin.delete_kv(key)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' deleted heartbeat miss count with key:' + key)

    @classmethod
    def deregister_secmon(cls, secmon_id):
        """Deletes the registered secmon once the count
           reaches BACKOFF_COUNT

        Args:
            secmon_id: id of the secmon to de-register

        Returns:
            None
        """
        url = 'http://' + 'localhost:9082/v1.0/secmon/secmondetails/' + secmon_id + '/'
        req = urllib2.Request(url)
        req.get_method = lambda:'DELETE'
        f = urllib2.urlopen(req)
        if f.getcode() == 204:
            configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' deregistered secmon with id:' + secmon_id)
        else:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' secmon with id:' + secmon_id + ' cannot be deleted')
