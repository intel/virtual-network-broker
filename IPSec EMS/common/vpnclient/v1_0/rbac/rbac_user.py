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
from vpnclient.v1_0.command_list import ListCommand
from vpnclient.v1_0.command_resource import CommandResource
from vpnclient.v1_0.rbac.utils_rbac import check_email, check_name_len

_COMMAND_COLUMNS = (
    'id',
    'username',
    'description',
    'password',
    'email',
)

_HTTP_RESOURCE = 'users'

_PK_COLUMN = 'id'


class CreateUser(CommandResource):
    """Create a RBAC User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'username',
            metavar='USERNAME',
            type=check_name_len,
            help=FH(_("Username of RBAC User")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of RBAC User")))

        parser.add_argument(
            '--password',
            required=True,
            help=FH(_("Password of RBAC User")))

        parser.add_argument(
            '--email',
            required=True,
            type=check_email,
            help=FH(_("Email of RBAC User")))

        return parser


class ShowUser(CommandResource):
    """Show information of a given RBAC User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_USER',
            help=FH(_("ID of RBAC User to search")))

        return parser


class ListUser(CommandResource):
    """List all RBAC Users"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateUser(CommandResource):
    """Update a given RBAC User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'id',
            metavar='RBAC_USER',
            help=FH(_("ID of RBAC User to update")))

        parser.add_argument(
            '--username',
            type=check_name_len,
            help=FH(_("Username of RBAC User")))

        parser.add_argument(
            '--password',
            help=FH(_("Password of RBAC User")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of RBAC User")))

        parser.add_argument(
            '--email',
            type=check_email,
            help=FH(_("Email of RBAC User")))

        return parser


class DeleteUser(CommandResource):
    """Delete a given RBAC User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_USER',
            help=FH(_("ID of RBAC User to delete")))

        return parser
