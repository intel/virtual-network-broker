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

import logging
from multiprocessing.connection import Client, Listener
from socket import error as socket_error

from services.api.serializers.vpn_choices import VPN_BIND
from services.ipsecenforcer.notification_for_register_deregister import \
    IPsecEnforcerRegistrationNotification
from services.ipsecenforcer.notification_vpn_configuration_update import (
    IPsecConfigUpdateNotification
)
from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo

LOG = logging.getLogger(__name__)


class IPsecEnforcerNotification(object):
    """This notification module notifies the IPSec enforcer about
any new peer IPsec Enforcer registrations or new in modules to
runs as a independent background process.

This process is started by a custom command. The command name is
'ipsecenforcernotify'. This custom command is defined in 'management'
module.
"""
    #
    # IPsecEnforcer Notification process socket information
    #
    process_fqdn = 'localhost'
    process_port = 8082

    @classmethod
    def listener(cls):
        """IPC Listener for IPsecEnforcer Notification"""
        LOG.info("IPsec Enforcer Notification agent started")

        # Listen for IPsec Enforcer Notification
        ipsec_enforcer_socket = Listener((cls.process_fqdn, cls.process_port))

        while True:
            conn = ipsec_enforcer_socket.accept()

            # Read data from socket
            data = conn.recv()

            notification_type = data.pop('notification_type')

            if notification_type == 'REGISTRATION':
                IPsecEnforcerRegistrationNotification.start(**data)
            elif notification_type == 'DEREGISTRATION':
                IPsecEnforcerRegistrationNotification.start(**data)
            elif notification_type == 'CONFIG_UPDATE':
                IPsecConfigUpdateNotification.record_update(**data)
            elif notification_type == 'CONFIG_DELETE':
                # Delete Notification only for VPNBind record
                IPsecConfigUpdateNotification.vpnbind_record_delete(**data)

    @classmethod
    def client(cls, resource, record=None, record_update=None):
        """IPC Client for Record Update or Delete

        Args:
            resource (str): name of the resource
            record (str): original record before updation
            record_update: record updates(only valid in case of PUT)
        """
        try:
            client = Client((cls.process_fqdn, cls.process_port))
        except socket_error:
            return

        if record_update is not None:
            notification_type = 'CONFIG_UPDATE'
        else:
            # As a Non-VPNBind record part of a VBNBind record is not allowed to
            # to be deleted, so there is no need to send delete notification of
            # Non-Bind to IPsecEnforcers.
            if resource not in VPN_BIND:
                return

            notification_type = 'CONFIG_DELETE'

        notification_message = {
            'notification_type': notification_type,
        }

        if resource is not None:
            notification_message.update({'resource': resource})

        if record is not None:
            notification_message.update({'record': record})

        if record_update is not None:
            notification_message.update({'record_update': record_update})

        # Send the notification_message to the IPsecEnforcer Notification
        # listener
        try:
            client.send(notification_message)
        except socket_error:
            return

    @classmethod
    def client_ipsecenforcer_register(cls, ipsecenforcer_id):
        """IPC Client for IPsecEnforcer Registration

        Args:
            ipsecenforcer_id: id of IPsecEnforcer
        """
        try:
            client = Client((cls.process_fqdn, cls.process_port))
        except socket_error:
            return

        mapping_records = (
            IPsecEnforcerInfo.get_ipsecenforcer_to_vpnendpoint_map(
                    ipsecenforcer_id)
        )

        notification_message = {
            'notification_type': 'REGISTRATION',
            'ipsecenforcer_id': ipsecenforcer_id,
            'mapping_records': mapping_records
        }

        # Send the notification_message to the IPsecEnforcer Notification
        # listener
        try:
            client.send(notification_message)
        except socket_error:
            return

    @classmethod
    def client_ipsecenforcer_deregister(cls, ipsecenforcer_id, mapping_records):
        """IPC Client for IPsecEnforcer De-Registration

        Args:
            ipsecenforcer_id: id of IPsecEnforcer
        """
        try:
            client = Client((cls.process_fqdn, cls.process_port))
        except socket_error:
            return

        notification_message = {
            'notification_type': 'DEREGISTRATION',
            'ipsecenforcer_id': ipsecenforcer_id,
            'mapping_records': mapping_records
        }

        # Send the notification_message to the IPsecEnforcer Notification
        # listener
        try:
            client.send(notification_message)
        except socket_error:
            return


