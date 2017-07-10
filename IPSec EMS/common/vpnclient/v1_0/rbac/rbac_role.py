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
    'rules',
    'groups',
)

_HTTP_RESOURCE = 'roles'

_PK_COLUMN = 'id'

_RULE_PERMISSIONS = (
        'VIEW',
        'ADD',
        'CHANGE',
        'DELETE',
)


class CreateRole(CommandResource):
    """Create a RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of RBAC Role")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of the RBAC Role")))

        return parser


class ShowRole(CommandResource):
    """Show information of a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role to search")))

        return parser


class ListRole(CommandResource):
    """Show information of a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateRole(CommandResource):
    """Update a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'id',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role to update")))

        parser.add_argument(
            'name',
            type=check_name_len,
            help=FH(_("Name of RBAC Role")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of RBAC Role")))

        return parser


class DeleteRole(CommandResource):
    """Delete a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role to delete")))

        return parser


class AddGroup(CommandResource):
    """Add RBAC Group to given RBAC Role"""
    cmd_columns = (
        'roles',
        'groups',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('groups',)
    pk_column = 'roles'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'roles',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role")))

        parser.add_argument(
            'groups',
            metavar='RBAC_GROUP',
            help=FH(_("ID of RBAC Group to add")))

        return parser


class RemoveGroup(CommandResource):
    """Remove RBAC Group from given RBAC Role"""
    cmd_columns = (
        'roles',
        'groups',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('groups',)
    pk_column = 'roles'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'roles',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role")))

        parser.add_argument(
            'groups',
            metavar='RBAC_GROUP',
            help=FH(_("ID of RBAC Group to remove")))

        return parser


class AddRule(CommandResource):
    """Add RBAC Rule to a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_request_attrs = (
        'roles',
        'resource_endpoint',
        'order',
        'permissions'
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('rules',)
    pk_column = 'roles'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'roles',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role")))

        parser.add_argument(
            '--resource-endpoint',
            metavar='RESOURCE_ENDPOINT',
            help=FH(_("Resource Endpoint")))

        parser.add_argument(
            '--order',
            type=int,
            help=FH(_("Order of the RBAC Rule")))

        parser.add_argument(
            '--permissions',
            action='append',
            choices=_RULE_PERMISSIONS,
            help=FH(_("Permissions for Resource Endpoint")))

        return parser


class RemoveRule(CommandResource):
    """Add RBAC Rule to a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_request_attrs = (
        'roles',
        'rules',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('rules',)
    pk_column = 'roles'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'roles',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role")))

        parser.add_argument(
            'rules',
            metavar='RBAC_RULE',
            help=FH(_("ID of RBAC Rule to delete")))

        return parser


class ChangeOrderRule(CommandResource):
    """Change order of RBAC Rule in a given RBAC Role"""
    cmd_columns = _COMMAND_COLUMNS
    http_request_attrs = (
        'roles',
        'rules',
        'orders',
    )
    http_resource = _HTTP_RESOURCE
    http_secondary_resources = ('rules', 'orders')
    pk_column = 'roles'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'roles',
            metavar='RBAC_ROLE',
            help=FH(_("ID of RBAC Role")))

        parser.add_argument(
            'rules',
            metavar='RBAC_RULE',
            help=FH(_("ID of RBAC Rule to delete")))

        parser.add_argument(
            'orders',
            metavar='RBAC_RULE_ORDER',
            help=FH(_("New order of the RBAC Rule")))

        return parser

