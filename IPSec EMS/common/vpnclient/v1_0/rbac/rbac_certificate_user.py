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

_COMMAND_COLUMNS = (
    'id',
    'subject_pattern',
    'description',
)

_HTTP_RESOURCE = 'users'

_PK_COLUMN = 'id'


class CreateCertificateUser(CommandResource):
    """Create a RBAC Certificate User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'subject-pattern',
            metavar='SUBJECT_PATTERN',
            help=FH(_("Pattern of Certificate's Subject or Alt. Name")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of RBAC Certificate User")))

        return parser


class ShowCertificateUser(CommandResource):
    """Show information of a given RBAC Certificate User"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_CERTIFICATE_USER',
            help=FH(_("ID of RBAC Certificate User to search")))

        return parser


class ListCertificateUser(CommandResource):
    """List all RBAC Certificate Users"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateCertificateUser(CommandResource):
    """Update a given RBAC CertificateUser"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'id',
            metavar='RBAC_CERTIFICATE_USER',
            help=FH(_("ID of RBAC Certificate User to update")))

        parser.add_argument(
            '--subject_pattern',
            help=FH(_("Pattern of Certificate's Subject or Alt. Name")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of RBAC Certificate User")))

        return parser


class DeleteCertificateUser(CommandResource):
    """Delete a given RBAC CertificateUser"""
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE
    pk_column = _PK_COLUMN

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='RBAC_CERTIFICATE_USER',
            help=FH(_("ID of RBAC Certificate User to delete")))

        return parser
