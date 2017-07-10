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

from __future__ import print_function

import argparse
from collections import OrderedDict
import gettext
import logging
import os
import sys


sys.path.append(os.path.abspath('..'))

from vpnclient.v1_0.rbac import (
    rbac_certificate_user, rbac_group, rbac_project, rbac_role, rbac_user
)
from vpnclient.v1_0.vpn import (
    ikepolicy, ipsecpolicy,
    vpnbindgrouptogroup, vpnbindgrouptolocalsite, vpnbindgrouptoremotesite,
    vpnbindlocalsitetolocalsite, vpnbindlocalsitetoremotesite,
    vpncacertificate, vpnendpointgroup, vpnendpointlocalsite,
    vpnendpointremotesite
)
from command_manager import CommandManager
from vpnclient import utils


# I18N
gettext.install('vpn_cmdclient', 'locale', unicode=True, names=['ngettext'])

VERSION = '1.0'
IPSEC_EMS_API_VERSION = '1.0'

# Supported commands in IPSec EMS API for Version 1 (v1)
# Each entry is of form ('commands-name': commandClass)
COMMAND_V1 = {
    'vpn-bindlocalsitetolocalsite-list':
        vpnbindlocalsitetolocalsite.ListVPNBindLocalSiteToLocalSite,
    'vpn-bindlocalsitetolocalsite-show':
        vpnbindlocalsitetolocalsite.ShowVPNBindLocalSiteToLocalSite,
    'vpn-bindlocalsitetolocalsite-create':
        vpnbindlocalsitetolocalsite.CreateVPNBindLocalSiteToLocalSite,
    'vpn-bindlocalsitetolocalsite-update':
        vpnbindlocalsitetolocalsite.UpdateVPNBindLocalSiteToLocalSite,
    'vpn-bindlocalsitetolocalsite-delete':
        vpnbindlocalsitetolocalsite.DeleteVPNBindLocalSiteToLocalSite,

    'vpn-bindlocalsitetoremotesite-list':
        vpnbindlocalsitetoremotesite.ListVPNBindLocalSiteToRemoteSite,
    'vpn-bindlocalsitetoremotesite-show':
        vpnbindlocalsitetoremotesite.ShowVPNBindLocalSiteToRemoteSite,
    'vpn-bindlocalsitetoremotesite-create':
        vpnbindlocalsitetoremotesite.CreateVPNBindLocalSiteToRemoteSite,
    'vpn-bindlocalsitetoremotesite-update':
        vpnbindlocalsitetoremotesite.UpdateVPNBindLocalSiteToRemoteSite,
    'vpn-bindlocalsitetoremotesite-delete':
        vpnbindlocalsitetoremotesite.DeleteVPNBindLocalSiteToRemoteSite,

    'vpn-bindgrouptogroup-list':
        vpnbindgrouptogroup.ListVPNBindGroupToGroup,
    'vpn-bindgrouptogroup-show':
        vpnbindgrouptogroup.ShowVPNBindGroupToGroup,
    'vpn-bindgrouptogroup-create':
        vpnbindgrouptogroup.CreateVPNBindGroupToGroup,
    'vpn-bindgrouptogroup-update':
        vpnbindgrouptogroup.UpdateVPNBindGroupToGroup,
    'vpn-bindgrouptogroup-delete':
        vpnbindgrouptogroup.DeleteVPNBindGroupToGroup,

    'vpn-bindgrouptolocalsite-list':
        vpnbindgrouptolocalsite.ListVPNBindGroupToLocalSite,
    'vpn-bindgrouptolocalsite-show':
        vpnbindgrouptolocalsite.ShowVPNBindGroupToLocalSite,
    'vpn-bindgrouptolocalsite-create':
        vpnbindgrouptolocalsite.CreateVPNBindGroupToLocalSite,
    'vpn-bindgrouptolocalsite-update':
        vpnbindgrouptolocalsite.UpdateVPNBindGroupToLocalSite,
    'vpn-bindgrouptolocalsite-delete':
        vpnbindgrouptolocalsite.DeleteVPNBindGroupToLocalSite,

    'vpn-bindgrouptoremotesite-list':
        vpnbindgrouptoremotesite.ListVPNBindGroupToRemoteSite,
    'vpn-bindgrouptoremotesite-show':
        vpnbindgrouptoremotesite.ShowVPNBindGroupToRemoteSite,
    'vpn-bindgrouptoremotesite-create':
        vpnbindgrouptoremotesite.CreateVPNBindGroupToRemoteSite,
    'vpn-bindgrouptoremotesite-update':
        vpnbindgrouptoremotesite.UpdateVPNBindGroupToRemoteSite,
    'vpn-bindgrouptoremotesite-delete':
        vpnbindgrouptoremotesite.DeleteVPNBindGroupToRemoteSite,

    'vpn-endpointlocalsite-list':
        vpnendpointlocalsite.ListVPNEndpointLocalSite,
    'vpn-endpointlocalsite-show':
        vpnendpointlocalsite.ShowVPNEndpointLocalSite,
    'vpn-endpointlocalsite-create':
        vpnendpointlocalsite.CreateVPNEndpointLocalSite,
    'vpn-endpointlocalsite-update':
        vpnendpointlocalsite.UpdateVPNEndpointLocalSite,
    'vpn-endpointlocalsite-delete':
        vpnendpointlocalsite.DeleteVPNEndpointLocalSite,

    'vpn-endpointgroup-list':
        vpnendpointgroup.ListVPNEndpointGroup,
    'vpn-endpointgroup-show':
        vpnendpointgroup.ShowVPNEndpointGroup,
    'vpn-endpointgroup-create':
        vpnendpointgroup.CreateVPNEndpointGroup,
    'vpn-endpointgroup-update':
        vpnendpointgroup.UpdateVPNEndpointGroup,
    'vpn-endpointgroup-delete':
        vpnendpointgroup.DeleteVPNEndpointGroup,

    'vpn-endpointremotesite-list':
        vpnendpointremotesite.ListVPNEndpointRemoteSite,
    'vpn-endpointremotesite-show':
        vpnendpointremotesite.ShowVPNEndpointRemoteSite,
    'vpn-endpointremotesite-create':
        vpnendpointremotesite.CreateVPNEndpointRemoteSite,
    'vpn-endpointremotesite-update':
        vpnendpointremotesite.UpdateVPNEndpointRemoteSite,
    'vpn-endpointremotesite-delete':
        vpnendpointremotesite.DeleteVPNEndpointRemoteSite,

    'vpn-cacertificate-list':
        vpncacertificate.ListVPNCACertificate,
    'vpn-cacertificate-show':
        vpncacertificate.ShowVPNCACertificate,
    'vpn-cacertificate-create':
        vpncacertificate.CreateVPNCACertificate,
    'vpn-cacertificate-update':
        vpncacertificate.UpdateVPNCACertificate,
    'vpn-cacertificate-delete':
        vpncacertificate.DeleteVPNCACertificate,

    'vpn-ikepolicy-list':
        ikepolicy.ListIKEPolicy,
    'vpn-ikepolicy-show':
        ikepolicy.ShowIKEPolicy,
    'vpn-ikepolicy-create':
        ikepolicy.CreateIKEPolicy,
    'vpn-ikepolicy-update':
        ikepolicy.UpdateIKEPolicy,
    'vpn-ikepolicy-delete':
        ikepolicy.DeleteIKEPolicy,

    'vpn-ipsecpolicy-list':
        ipsecpolicy.ListIPsecPolicy,
    'vpn-ipsecpolicy-show':
        ipsecpolicy.ShowIPsecPolicy,
    'vpn-ipsecpolicy-create':
        ipsecpolicy.CreateIPsecPolicy,
    'vpn-ipsecpolicy-update':
        ipsecpolicy.UpdateIPsecPolicy,
    'vpn-ipsecpolicy-delete':
        ipsecpolicy.DeleteIPsecPolicy,

    'rbac-user-list':
        rbac_user.ListUser,
    'rbac-user-show':
        rbac_user.ShowUser,
    'rbac-user-create':
        rbac_user.CreateUser,
    'rbac-user-update':
        rbac_user.UpdateUser,
    'rbac-user-delete':
        rbac_user.DeleteUser,

    'rbac-certificateuser-list':
        rbac_certificate_user.ListCertificateUser,
    'rbac-certificateuser-show':
        rbac_certificate_user.ShowCertificateUser,
    'rbac-certificateuser-create':
        rbac_certificate_user.CreateCertificateUser,
    'rbac-certificateuser-update':
        rbac_certificate_user.UpdateCertificateUser,
    'rbac-certificateuser-delete':
        rbac_certificate_user.DeleteCertificateUser,

    'rbac-project-list':
        rbac_project.ListProject,
    'rbac-project-show':
        rbac_project.ShowProject,
    'rbac-project-create':
        rbac_project.CreateProject,
    'rbac-project-update':
        rbac_project.UpdateProject,
    'rbac-project-delete':
        rbac_project.DeleteProject,


    'rbac-role-list':
        rbac_role.ListRole,
    'rbac-role-show':
        rbac_role.ShowRole,
    'rbac-role-create':
        rbac_role.CreateRole,
    'rbac-role-update':
        rbac_role.UpdateRole,
    'rbac-role-delete':
        rbac_role.DeleteRole,
    'rbac-role-add-group':
        rbac_role.AddGroup,
    'rbac-role-remove-group':
        rbac_role.RemoveGroup,
    'rbac-role-add-rule':
        rbac_role.AddRule,
    'rbac-role-delete-rule':
        rbac_role.RemoveRule,


    'rbac-group-list':
        rbac_group.ListGroup,
    'rbac-group-show':
        rbac_group.ShowGroup,
    'rbac-group-create':
        rbac_group.CreateGroup,
    'rbac-group-update':
        rbac_group.UpdateGroup,
    'rbac-group-delete':
        rbac_group.DeleteGroup,
    'rbac-group-add-user':
        rbac_group.AddUser,
    'rbac-group-remove-user':
        rbac_group.RemoveUser,
}

# Activate a specific version commands
COMMANDS = {IPSEC_EMS_API_VERSION: OrderedDict(sorted(COMMAND_V1.items()))}


class Shell(object):
    # verbose logging levels
    WARNING_LEVEL = 0
    INFO_LEVEL = 1
    DEBUG_LEVEL = 2
    CONSOLE_MESSAGE_FORMAT = '%(message)s'
    DEBUG_MESSAGE_FORMAT = '%(levelname)s: %(name)s %(message)s'
    log = logging.getLogger(__name__)

    def __init__(self, apiversion):

        self.subcommand = None
        self.subcommand_help = None
        self.subcommand_class = None
        self.action = None
        self.resource = None
        self.prog_name = None
        self.description = None
        self.epilog = None

        self.commands = COMMANDS
        self.service = 'EMS'
        self.prog_name = 'ipsec-ems'
        self.api_version = apiversion

        self.DEFAULT_VERBOSE_LEVEL = self.INFO_LEVEL

    def parse_default_args(self):
        """An argparse parser for the IPsec EMS CLI.

        Returns: An argparse parser
        """
        if self.subcommand:
            self.prog_name += ' ' + self.subcommand
            self.epilog = ''
            self.description = self.subcommand_class.__doc__
        else:
            self.description = _("Command-line interface to the IPsec EMS APIs")

            commandlist = _("Commands for IPSEC EMS API v1.0:\n")
            prev_cmd_prefix = ''
            for key, value in COMMANDS[self.api_version].items():
                cmd_prefix = key.split("-")[1]
                if (cmd_prefix != prev_cmd_prefix) and (prev_cmd_prefix != ''):
                    prev_cmd_prefix = cmd_prefix
                    commandlist += '\n\n'
                else:
                    prev_cmd_prefix = cmd_prefix
                    commandlist += '\n'
                commandlist += '{0:40}{1}'.format(key, value.__doc__)

            self.epilog = commandlist

        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=self.description,
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=self.epilog,
        )

        # Version of IPsec EMS Management APIs.
        parser.add_argument(
            '--version',
            action='version',
            version=str(IPSEC_EMS_API_VERSION), )

        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help=_("Increase verbosity of output and show tracebacks on\n"
                   "errors."))

        # Fill the argparse parser with subcommand's attributes
        if self.subcommand:
            sys.argv = sys.argv[1:]

            parser = self.subcommand_class().add_known_arguments(parser)
            if self.subcommand_help:
                return parser

        # All the below are the default arguments for a request

        # IP or FQDN of one of the EMS
        parser.add_argument(
            '--ipsec-ems-fqdn',
            default=utils.env('IPSEC_EMS_FQDN'),
            type=utils.check_fqdn,
            help=_("IPsec EMS Broker FQDN or IP Address\n"
                   "(Defaults to Env: IPSEC_EMS_FQDN)"))

        # Scope or Domain of EMS
        # Default is 'main'
        parser.add_argument(
            '--namespace',
            metavar='<namespace>',
            default=utils.env('IPSEC_EMS_NAMESPACE', default='main'),
            type=utils.check_namespace,
            help=_("Namespace(or Domain)\n"
                   "(Defaults to Env: IPSEC_EMS_NAMESPACE)"))

        # Authentication with IPsec EMS with auth-token
        parser.add_argument(
            '--auth-token',
            metavar='<auth-token>',
            default=utils.env('IPSEC_EMS_AUTH_TOKEN', default=''),
            help=_("Authentication token\n"
                   "(Defaults to Env: IPSEC_EMS_AUTH_TOKEN)"))

        # Below attributes are for HTTPS communication with IPsec EMS
        parser.add_argument(
            '--cert',
            metavar='<certificate>',
            default=utils.env('IPSEC_EMS_CERT'),
            type=utils.check_cert,
            help=_("Path of certificate file to use in SSL connection.\n"
                   "This file can optionally be prepended with the \n"
                   "private key.\n"
                   "(Defaults to Env: IPSEC_EMS_CERT)"))

        parser.add_argument(
            '--key',
            metavar='<cert-key>',
            default=utils.env('IPSEC_EMS_KEY'),
            type=utils.check_key,
            help=_("Path of client key to use in SSL connection. This\n"
                   "option is not necessary if your key is prepended to\n"
                   "to your certificate file.\n"
                   "(Defaults to Env: IPSEC_EMS_KEY)"))

        parser.add_argument(
            '--cacert',
            metavar='<ca-certificate>',
            default=utils.env('IPSEC_EMS_CACERT', default=''),
            help=_("Specify a CA bundle file to use in verifying a TLS\n"
                   "(https) server's certificate.\n"
                   "(Defaults to Env: IPSEC_EMS_CACERT)"))

        parser.add_argument(
            '--insecure',
            type=bool,
            choices=[True, False],
            default=utils.env('IPSEC_EMS_INSECURE', default=''),
            help=_("Explicitly allow cli client to perform \"insecure\"\n"
                   "SSL (https) requests. The server's certificate will\n"
                   "not be verified against any certificate authorities.\n"
                   "This option should be used with caution.\n"
                   "(Defaults to Env: IPSEC_EMS_KEY, Value: True)"))

        parser.add_argument(
            '--http-timeout',
            metavar='<seconds>',
            default=utils.env('IPSEC_EMS_HTTP_TIMEOUT', default=''),
            type=utils.check_http_timeout,
            help=_("Timeout in seconds to wait for an HTTP response.\n"
                   "Defaults to Env: IPSEC_EMS_HTTP_TIMEOUT or None if\n"
                   "not specified."))

        return parser

    @staticmethod
    def validate_auth_attributes(var):
        """Validate authentication and cert. of argparse

        Args:
            var (An argparse parser): argparse parser with attribute's value

        Returns:
            None
        """
        # Authentication checks
        utils.check_if_empty(var.get('auth_strategy'), 'auth-strategy')
        if var.get('auth_strategy') == 'credential':
            utils.check_if_empty(var.get('username'), 'username')
            utils.check_if_empty(var.get('password'), 'password')
        elif var.get('auth_strategy') == 'token':
            utils.check_if_empty(var.get('auth_token'), 'auth-token')

        # Certificate checks
        if var.get('insecure'):

            if var.get('cacert'):
                if not os.path.exists(var.get('cacert')):
                    print(_('cacert is a not a valid path or file'))

    def run(self, argv):
        """Equivalent to the main program for the application.

        Args:
            argv (list of str): input arguments and options
        """
        try:
            index = 0
            command_pos = -1
            help_pos = -1
            for arg in argv:
                if arg in self.commands[self.api_version]:
                    if command_pos == -1:
                        command_pos = index
                        self.subcommand = arg
                        self.subcommand_class = \
                            self.commands.get(self.api_version).get(arg)
                elif arg in ('-h', '--help', 'help'):
                    if help_pos == -1:
                        help_pos = index
                index += 1
            if -1 < command_pos < help_pos:
                self.subcommand_help = True
            elif -1 < help_pos < command_pos:
                self.subcommand = None
            else:
                self.subcommand_help = False

            # Parse all the input arguments
            parser = self.parse_default_args()

            # Convert argparse to dict
            var = vars(parser.parse_args())

            # Validate some of the attributes
            self.validate_auth_attributes(var)

            self.subcommand_class().verify_arguments(var)

            # Find the command resource and action from the subcommand
            action = utils.find_subcommand_action(self.subcommand)

            http_resource, http_secondary_resources, cmd_columns, pk_column = (
                self.subcommand_class().get_http_resource_and_cmd_columns_and_pk())

            cmd_manager = CommandManager(http_resource,
                                         http_secondary_resources,
                                         var,
                                         self.api_version,
                                         cmd_columns,
                                         pk_column)

            attr_dict = self.subcommand_class().argparse_to_http_dict(var)

            func = getattr(cmd_manager, action)

            func(attr_dict)

            # self.configure_logging()
            # self.interactive_mode = not remainder
            # self.initialize_app(remainder)
        except Exception as err:
            # if self.verbose_level == self.DEBUG_LEVEL:
            # self.log.exception(unicode(err))
            print(err)
            # raise
            # else:
            #     self.log.error(unicode(err))
            return 1
            # result = self.run_subcommand(remainder)
            # return result

    def configure_logging(self):
        """Create logging handlers for any log output."""
        root_logger = logging.getLogger('')

        # Set up logging to a file
        root_logger.setLevel(logging.DEBUG)

        # Send higher-level messages to the console via stderr
        console = logging.StreamHandler(self.stderr)
        console_level = {self.WARNING_LEVEL: logging.WARNING,
                         self.INFO_LEVEL: logging.INFO,
                         self.DEBUG_LEVEL: logging.DEBUG,
                         }.get(self.options.verbose_level, logging.DEBUG)
        # The default log level is INFO, in this situation, set the
        # log level of the console to WARNING, to avoid displaying
        # useless messages. This equals using "--quiet"
        if console_level == logging.INFO:
            console.setLevel(logging.WARNING)
        else:
            console.setLevel(console_level)
        if logging.DEBUG == console_level:
            formatter = logging.Formatter(self.DEBUG_MESSAGE_FORMAT)
        else:
            formatter = logging.Formatter(self.CONSOLE_MESSAGE_FORMAT)
        logging.getLogger('iso8601.iso8601').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        console.setFormatter(formatter)
        root_logger.addHandler(console)
        return


def main(argv=sys.argv[1:]):
    try:
        return Shell(IPSEC_EMS_API_VERSION).run(argv)
    except KeyboardInterrupt:
        print(_("Exit requested"), file=sys.stdout)
    except Exception as e:
        print(unicode(e))
        return 1


if __name__ == "__main__":  # CLI client starts here
    sys.exit(main(sys.argv[1:]))
