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
import pdb

from secmonclient.utils import prepare_body
from secmonclient.v1_0.vpn import command_column

COMMAND_COLUMNS = []
HTTP_RESOURCE = 'resources'


class CommandResource(object):
    __metaclass__ = abc.ABCMeta

    resource = 'resource'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        pass

    @staticmethod
    def verify_arguments(attrs):
        pass

    def argparse_to_http_dict(self, parsed_args, resource):
        #self._column = getattr(command_column,
        #                        '{0}_COLUMNS'.format(resource.upper()))
#        pdb.set_trace()
        return prepare_body(parsed_args, self.cmd_columns)

    def get_http_resource_and_cmd_columns(self):
        return self.http_resource, self.cmd_columns
