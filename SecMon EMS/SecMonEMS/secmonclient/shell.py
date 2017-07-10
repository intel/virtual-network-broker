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
import pdb
from collections import OrderedDict
import gettext
import logging
import os
import sys
# from django.utils.translation import ugettext as _

sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import (
     collector, collectorset, classificationobject, netflowassociation,
     netflowconfig, netflowmonitor, policy, rawforwardassociation, ruleobject,
     scope, secmondetails, sflowassociation, sflowconfig
)
from secmonclient.v1_0.vpn import utils_vpn

from command_manager import CommandManager
from secmonclient import utils

# I18N
gettext.install('vpn_cmdclient', 'locale', unicode=True, names=['ngettext'])

VERSION = '1.0'
IPSEC_EMS_API_VERSION = '1.0'

# Supported commands in IPSec EMS API for Version 1 (v1)
# Each entry is of form ('commands-name': commandClass)
COMMAND_V1 = {
    'collector-create':
        collector.CreateCollector,
    'collector-list':
        collector.ListCollector,
    'collector-show':
        collector.ShowCollector,
    'collector-update':
        collector.UpdateCollector,
    'collector-delete':
        collector.DeleteCollector,
    'policy-create':
        policy.CreatePolicy,
    'policy-list':
        policy.ListPolicy,
    'policy-show':
        policy.ShowPolicy,
    'policy-update':
        policy.UpdatePolicy,
    'policy-delete':
        policy.DeletePolicy,
    'rawforwardassociation-create':
        rawforwardassociation.CreateRawForwardAssociation,
    'rawforwardassociation-list':
        rawforwardassociation.ListRawForwardAssociation,
    'rawforwardassociation-show':
        rawforwardassociation.ShowRawForwardAssociation,
    'rawforwardassociation-update':
        rawforwardassociation.UpdateRawForwardAssociation,
    'rawforwardassociation-delete':
        rawforwardassociation.DeleteRawForwardAssociation,
    'ruleobject-create':
        ruleobject.CreateRuleObject,
    'ruleobject-list':
        ruleobject.ListRuleObject,
    'ruleobject-show':
        ruleobject.ShowRuleObject,
    'ruleobject-update':
        ruleobject.UpdateRuleObject,
    'ruleobject-delete':
        ruleobject.DeleteRuleObject,
    'scope-create':
        scope.CreateScope,
    'scope-list':
        scope.ListScope,
    'scope-show':
        scope.ShowScope,
    'scope-update':
        scope.UpdateScope,
    'scope-delete':
        scope.DeleteScope,
    'secmondetails-create':
        secmondetails.CreateSecmonDetails,
    'secmondetails-list':
        secmondetails.ListSecmonDetails,
    'secmondetails-show':
        secmondetails.ShowSecmonDetails,
    'secmondetails-update':
        secmondetails.UpdateSecmonDetails,
    'secmondetails-delete':
        secmondetails.DeleteSecmonDetails,
    'sflowassociation-create':
        sflowassociation.CreateSFlowAssociation,
    'sflowassociation-list':
        sflowassociation.ListSFlowAssociation,
    'sflowassociation-show':
        sflowassociation.ShowSFlowAssociation,
    'sflowassociation-update':
        sflowassociation.UpdateSFlowAssociation,
    'sflowassociation-delete':
        sflowassociation.DeleteSFlowAssociation,
    'sflowconfig-create':
        sflowconfig.CreateSflowConfig,
    'sflowconfig-list':
        sflowconfig.ListSflowConfig,
    'sflowconfig-show':
        sflowconfig.ShowSflowConfig,
    'sflowconfig-update':
        sflowconfig.UpdateSflowConfig,
    'sflowconfig-delete':
        sflowconfig.DeleteSflowConfig,
    'collectorset-create':
        collectorset.CreateCollectorset,
    'collectorset-list':
        collectorset.ListCollectorset,
    'collectorset-show':
        collectorset.ShowCollectorset,
    'collectorset-update':
        collectorset.UpdateCollectorset,
    'collectorset-delete':
        collectorset.DeleteCollectorset,
    'classificationobject-create':
        classificationobject.CreateClassificationObject,
    'classificationobject-list':
        classificationobject.ListClassificationObject,
    'classificationobject-show':
        classificationobject.ShowClassificationObject,
    'classificationobject-update':
        classificationobject.UpdateClassificationObject,
    'classificationobject-delete':
        classificationobject.DeleteClassificationObject,
    'netflowassociation-create':
        netflowassociation.CreateNetFlowAssociation,
    'netflowassociation-list':
        netflowassociation.ListNetFlowAssociation,
    'netflowassociation-show':
        netflowassociation.ShowNetFlowAssociation,
    'netflowassociation-update':
        netflowassociation.UpdateNetFlowAssociation,
    'netflowassociation-delete':
        netflowassociation.DeleteNetFlowAssociation,
    'netflowconfig-create':
        netflowconfig.CreateNetFlowConfig,
    'netflowconfig-list':
        netflowconfig.ListNetFlowConfig,
    'netflowconfig-show':
        netflowconfig.ShowNetFlowConfig,
    'netflowconfig-update':
        netflowconfig.UpdateNetFlowConfig,
    'netflowconfig-delete':
        netflowconfig.DeleteNetFlowConfig,
    'netflowmonitor-create':
        netflowmonitor.CreateNetFlowMonitor,
    'netflowmonitor-list':
        netflowmonitor.ListNetFlowMonitor,
    'netflowmonitor-show':
        netflowmonitor.ShowNetFlowMonitor,
    'netflowmonitor-update':
        netflowmonitor.UpdateNetFlowMonitor,
    'netflowmonitor-delete':
        netflowmonitor.DeleteNetFlowMonitor
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
        self.prog_name = 'configagent-ems'
        self.api_version = apiversion

        self.DEFAULT_VERBOSE_LEVEL = self.INFO_LEVEL

    def parse_default_args(self):
        """An argparse parser for the ConfigAgent EMS CLI.

        Returns: An argparse parser
        """
#        pdb.set_trace()
        if self.subcommand:
            self.prog_name += ' ' + self.subcommand
            self.epilog = ''
            self.description = self.subcommand_class.__doc__
        else:
            self.description = _("Command-line interface to the ConfigAgent EMS APIs")
            commandlist = _("Commands for ConfigAgent EMS API v1.0:\n")
            new_line = 5
            for key, value in COMMANDS[self.api_version].items():
                commandlist += '{0:40}{1}\n'.format(key, value.__doc__)
                new_line -= 1
                if new_line < 1:
                    commandlist += '\n'
                    new_line = 5

            self.epilog = commandlist

        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=self.description,
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=self.epilog,
        )

        # Version of ConfigAgent EMS Management APIs.
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
#        pdb.set_trace()
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
            help=_("ConfigAgent EMS IP Address\n"
                   "(Defaults to Env: IPSEC_EMS_FQDN)"))

        # Scope or Domain of EMS
        # Default is 'main'
        parser.add_argument(
            '--namespace',
            metavar='<namespace>',
            default='secmon',
            type=utils.check_namespace,
            help=_("Namespace(or Domain)\n"
                   "(Defaults to secmon"))

# ---------------------not done-----------------------
        # Authentication with IPsec EMS
        # auth-strategy :
        #   'credential' will just use username/password
        #   'token' will just use auth-token
#        parser.add_argument(
#            '--auth-strategy',
#            default=utils.env('IPSEC_EMS_AUTH_STRATEGY',
#                              default='credential'),
#            choices=['token', 'credential'],
#            type=utils.check_auth_strategy,
#            help=_("Authentication strategy\n"
#                   "(Defaults to Env: IPSEC_EMS_AUTH_STRATEGY, Value: "
#                   "credential)"))

#        parser.add_argument(
#            '--username',
#            metavar='<auth-username>',
#            default=utils.env('IPSEC_EMS_USERNAME'),
#            help=_("Authentication username\n"
#                   "(Defaults to Env: IPSEC_EMS_USERNAME)"))

#        parser.add_argument(
#            '--password',
#            metavar='<auth-password>',
#            default=utils.env('IPSEC_EMS_PASSWORD'),
#            help=_("Authentication password\n"
#                   "(Defaults to Env: IPSEC_EMS_PASSWORD)"))

#        parser.add_argument(
#            '--auth-token',
#            metavar='<auth-token>',
#            default=utils.env('IPSEC_EMS_AUTH_TOKEN', default=''),
#            help=_("Authentication token\n"
#                   "(Defaults to Env: IPSEC_EMS_AUTH_TOKEN)"))

        # Below attributes are for HTTPS communication with IPsec EMS
#        parser.add_argument(
#            '--cert',
#            metavar='<certificate>',
#            default=utils.env('IPSEC_EMS_CERT'),
#            type=utils.check_cert,
#            help=_("Path of certificate file to use in SSL connection.\n"
#                   "This file can optionally be prepended with the \n"
#                   "private key.\n"
#                   "(Defaults to Env: IPSEC_EMS_CERT)"))

#        parser.add_argument(
#            '--key',
#            metavar='<cert-key>',
#            default=utils.env('IPSEC_EMS_KEY'),
#            type=utils.check_key,
#            help=_("Path of client key to use in SSL connection. This\n"
#                   "option is not necessary if your key is prepended to\n"
#                   "to your certificate file.\n"
#                   "(Defaults to Env: IPSEC_EMS_KEY)"))

#        parser.add_argument(
#            '--cacert',
#            metavar='<ca-certificate>',
#            default=utils.env('IPSEC_EMS_CACERT', default=''),
#            help=_("Specify a CA bundle file to use in verifying a TLS\n"
#                   "(https) server's certificate.\n"
#                   "(Defaults to Env: IPSEC_EMS_CACERT)"))

#        parser.add_argument(
#            '--insecure',
#            type=bool,
#            choices=[True, False],
#            default=utils.env('IPSEC_EMS_INSECURE', default=''),
#            help=_("Explicitly allow cli client to perform \"insecure\"\n"
#                   "SSL (https) requests. The server's certificate will\n"
#                   "not be verified against any certificate authorities.\n"
#                   "This option should be used with caution.\n"
#                   "(Defaults to Env: IPSEC_EMS_KEY, Value: True)"))

#        parser.add_argument(
#            '--http-timeout',
#            metavar='<seconds>',
#            default=utils.env('IPSEC_EMS_HTTP_TIMEOUT', default=''),
#            type=utils.check_http_timeout,
#            help=_("Timeout in seconds to wait for an HTTP response.\n"
#                   "Defaults to Env: IPSEC_EMS_HTTP_TIMEOUT or None if\n"
#                   "not specified."))

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
#        pdb.set_trace()
        try:
#            print("inside run:",argv)
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
#            pdb.set_trace()
            # Parse all the input arguments
#            pdb.set_trace()
#            print("arg processed")
            parser = self.parse_default_args()
#            print("parse_default_args")
            # Convert argparse to dict
            var = vars(parser.parse_args())
#            print("vars(parser.parse_args())")
#            var = string_to_integer_field_mapping(var1)
#            # Validate some of the attributes
#            self.validate_auth_attributes(var)

#            pdb.set_trace()
#            self.subcommand_class().verify_arguments(var)

            # Find the command resource and action from the subcommand
            action, cmd_resource = utils.find_subcommand_resource_and_action(
                self.subcommand)
#            print("find_subcommand_resource_and_action")
#            pdb.set_trace()
            if action == 'create' or action == 'update':
                var = utils_vpn.string_to_integer_field_mapping(var)
#            print("string_to_integer_field_mapping")
            self.subcommand_class().verify_arguments(var)
#            print("verify_arguments")
#            pdb.set_trace()
#            if action=='list' or action=='show':
#                var = utils_vpn.integer_to_string_mapping(var)
            http_resource, cmd_columns = (
                self.subcommand_class().get_http_resource_and_cmd_columns())
#            print("get_http_resource_and_cmd_columns")
            cmd_manager = CommandManager(http_resource,
                                         var,
                                         self.api_version,
                                         cmd_columns)
#            print("CommandManager")
            attr_dict = self.subcommand_class().argparse_to_http_dict(
                    var,
                    http_resource)
#            print("argparse_to_http_dict")

#            pdb.set_trace()

            func = getattr(cmd_manager, action)
#            print("getattr")
            func(attr_dict)
#            print("func")
#            data_recevied = cmd_manager.create(attr_dict)
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
