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

import abc

from vpnclient.utils import prepare_body


HTTP_RESOURCE = 'resources'
PK_COLUMN = ''
COMMAND_COLUMNS = ()
HTTP_SECONDARY_RESOURCES = ()


class CommandResource(object):
    __metaclass__ = abc.ABCMeta

    resource = 'resource'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE
    pk_column = PK_COLUMN
    http_secondary_resources = ()
    http_request_attrs = ()

    @staticmethod
    def add_known_arguments(parser):
        pass

    @staticmethod
    def verify_arguments(attrs):
        pass

    def argparse_to_http_dict(self, parsed_args):
        if self.http_request_attrs:
            return prepare_body(parsed_args, self.http_request_attrs)
        return prepare_body(parsed_args, self.cmd_columns)

    def get_http_resource_and_cmd_columns_and_pk(self):
        return self.http_resource, self.http_secondary_resources, \
               self.cmd_columns, self.pk_column
