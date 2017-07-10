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
from vpnclient.v1_0.rbac.utils_rbac import check_name_len

_COMMAND_COLUMNS = (
    'id',
    'name',
    'description',
    'users',
    'certificate_users',
)

_HTTP_RESOURCE = 'groups'

_PK_COLUMN = 'id'


class CreateGroup(CommandResource):
    """Create a RBAC Group"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'name',
                metavar='NAME',
                type=check_name_len,
                help=FH(_("Name of RBAC Group")))

        parser.add_argument(
                '--description',
                help=FH(_("Description of RBAC Group")))

        return parser


class ShowGroup(CommandResource):
    """Show information of a given RBAC Group"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'id',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group to search")))

        return parser


class ListGroup(CommandResource):
    """List all RBAC Groups"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateGroup(CommandResource):
    """Update a given RBAC Group"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'id',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group to update")))

        parser.add_argument(
                '--name',
                metavar='NAME',
                type=check_name_len,
                help=FH(_("Name of RBAC Group")))

        parser.add_argument(
                '--description',
                help=FH(_("Description of RBAC Group")))

        return parser


class DeleteGroup(CommandResource):
    """Delete a given RBAC Group"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'id',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group to delete")))

        return parser


class AddUser(CommandResource):
    """Add RBAC User to a given RBAC Group"""
    cmd_columns = (
        'groups',
        'users',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('users',)
    pk_column = 'groups'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'groups',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group")))

        parser.add_argument(
                'users',
                metavar='RBAC_USER',
                help=FH(_("ID of RBAC User")))

        return parser


class RemoveUser(CommandResource):
    """Remove RBAC User from a given RBAC Group"""
    cmd_columns = (
        'groups',
        'users',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('users',)
    pk_column = 'groups'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'groups',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group")))

        parser.add_argument(
                'users',
                metavar='RBAC_USER',
                help=FH(_("ID of RBAC User")))

        return parser


class AddCertificateUser(CommandResource):
    """Add RBAC Certificate User to a given RBAC Group"""
    cmd_columns = (
        'groups',
        'certificate_users',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('certificate_users',)
    pk_column = 'groups'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'groups',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group")))

        parser.add_argument(
                'certificate_users',
                metavar='RBAC_CERTIFICATE_USER',
                help=FH(_("ID of RBAC Certificate User to add")))

        return parser


class RemoveCertificateUser(CommandResource):
    """Remove RBAC Certificate User from a given RBAC Group"""
    cmd_columns = (
        'groups',
        'certificate_users',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('certificate_users',)
    pk_column = 'groups'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
                'groups',
                metavar='RBAC_GROUP',
                help=FH(_("ID of RBAC Group")))

        parser.add_argument(
                'certificate_users',
                metavar='RBAC_CERTIFICATE_USER',
                help=FH(_("ID of RBAC Certificate User to delete")))

        return parser
