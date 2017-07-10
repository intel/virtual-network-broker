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
import pdb
from multiprocessing.connection import Client, Listener

from ConfigDB.secmon_notify.secmon_notification import (
    SecMonUpdateNotification
)
import configfile
import inspect
#LOG = configfile.configlogging()

class SecMonNotification(object):
    """This notification module notifies the SecMon about
any change in secmon configuration data.

This process is started by a custom command. The command name is
'emsnotify'. This custom command is defined in 'management'
module.
"""
    #
    # EMS Notification process socket information
    #
    process_fqdn = 'localhost'
    process_port = 9000

    @classmethod
    def listener(cls):
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + " SecMon Notification agent started")
        # Listen for EMS Notification
        secmon_socket = Listener((cls.process_fqdn, cls.process_port))
        while True:
            conn = secmon_socket.accept()
            # Read data from socket
            data = conn.recv()
            configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' connection received from client')
            SecMonUpdateNotification.record_update(**data)

    @classmethod
    def client(cls, row_id, resource, operation, row_data=None):
        """
        Args:
            row_id: id of updated row
            resource: resource name of updated row
            operation: operation performed on row
            row_data: provided for delete operation
        Returns:
        """
        client = Client((cls.process_fqdn, cls.process_port))
        notification_message = {'row_id': row_id}
        notification_message['resource'] = resource
        notification_message['operation'] = operation
        if operation == 'DELETE':
            notification_message['row_data'] = row_data
        client.send(notification_message)
        configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' notification sent by client')
