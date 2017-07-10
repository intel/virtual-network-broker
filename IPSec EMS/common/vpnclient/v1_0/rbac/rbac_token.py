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

from vpnclient.utils import FH
from vpnclient.v1_0.command_resource import CommandResource
from vpnclient.v1_0.rbac.utils_rbac import check_name_len

_COMMAND_COLUMNS = (
    'id',
    'auth_token',
    'users_id',
    'expiry_time',
    'certificate_users',
)

_HTTP_RESOURCE = 'tokens'

_PK_COLUMN = 'id'


class CreateUser(CommandResource):
    """Generate a RBAC Authentication Token"""
    cmd_columns = _COMMAND_COLUMNS
    http_request_attrs = (
        'username',
        'password',
    )
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                '--username',
                metavar='USERNAME',
                type=check_name_len,
                required=True,
                help=FH(_("Username of RBAC User")))

        parser.add_argument(
                '--password',
                metavar='PASSWORD',
                required=True,
                help=FH(_("Password of RBAC User")))

        return parser


class DeleteUser(CommandResource):
    """Revoke a RBAC Authentication Token"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        pass
