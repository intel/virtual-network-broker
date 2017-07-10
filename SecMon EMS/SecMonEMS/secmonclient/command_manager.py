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

import csv
import httplib as http_status_code
import json
import os
import sys
from operator import itemgetter
import pdb

# from django.utils.translation import ugettext as _
from prettytable import PrettyTable
from requests.auth import HTTPBasicAuth

from cli_cfg import PORT
from cli_cfg import WEB_PROTOCOL
from secmonclient.command_to_http_endpoint_map import COMMAND_TO_HTTP_ENDPOINT

sys.path.append(os.path.abspath('..'))
from secmonclient.http_client import HTTPClient
from secmonclient.v1_0.vpn import (command_column,
                                   utils_vpn)


class CommandManager:
    """Command Manager constructs the http request to be sent to EMS
    server and also prints the http response received from the
    server.

    It extracts the attributes value from the argparse and
    fills the http request.

    It calls HTTPClient to send the request and get back the response.

    It decides which method of HTTP request based on the type of
    commands:

    create:     POST
    show :      GET
    list :      GET
    update :    PUT
    delete:     DELETE

    It provides three options(csv, html, table) to format the http
    response received from the server.
    """

    def __init__(self, http_resource, argparse, version, cmd_columns):
        self.http_request = {}
        # Communication Protocol and Port for communication with EMS
        protocol = WEB_PROTOCOL
        port = PORT
#        service = 'ipsecvpn'
#        Default Headers
        self.http_request['headers'] = {
#        'User-Agent': 'ipsec-ems-client',
         'Content-type': 'application/json'
                                       }

        # REST API Version
        self._version = 'v' + str(float(version))

        # Domain or Namespace of EMS
        self._namespace = argparse.get('namespace')

        # Construct the URL using api version(e.g. v1), namespace, service type
        # and resource type.
        # e.g. https://ems.com:443/v1.0/main/collector
        self._url_prefix = \
            '{0}://{1}:{2}/{3}/{4}/'.format(protocol,
                                            argparse.get('ipsec_ems_fqdn'),
                                            port,
                                            self._version,
                                            self._namespace,
                                            )
        self.http_request['url'] = self._url_prefix + http_resource + '/'

#        # Header Authentication token OR username:password
#        if argparse.get('auth_strategy') is 'token':

#            self.http_request['headers'] = (
#                {
#                    'X-Auth-Token': argparse.get('token')
#                }
#            )
#        elif argparse.get('auth_strategy') is 'credential':
#            self._username = argparse.get('username')
#            self._password = argparse.get('password')
#            self.http_request['auth'] = HTTPBasicAuth(self._username,
#                                                      self._password)

#        # HTTPS certificate and private key(optional if certificate
#        # already contains the key)
#        if argparse.get('key'):
#            self.http_request['cert'] = (argparse.get('cert'),
#                                         argparse.get('key'))
#        else:
#            self.http_request['cert'] = argparse.get('cert')

#        # Verifying certificate with CA
#        if argparse.get('cacert'):
#            self.http_request['verify'] = argparse.get('cacert')

#        # HTTP request timeout
#        if argparse.get('http_timeout'):
#            self.http_request['timeout'] = argparse.get('http_timeout')

        # Below are HTTP response(output) formatting options

        # Show details in case of list commands
        self.show_details = argparse.get('show_details')

        # Columns/Field names for the resource. It is used by
        # commands(list, show, create, update)
        self.column = cmd_columns

        # Requested columns/fields to be displayed in the output
        self.fields = argparse.get('fields')
        # Requested columns/fieLds must be a subset of resource
        # original fields
        if self.fields:
            if not set(self.fields).issubset(set(self.column)):
                print("Specified field(s) list {0} must be a subset"
                      "of the resource field's list {1}".format(self.fields,
                                                                self.column))
            sys.exit(0)

        # List of column/field to on the basis to sort the output
        self.sort_key = argparse.get('sort_key')

        # Sorting directions(asc or desc) for the above keys
        self.sort_direction = argparse.get('sort_direction')

        # Sort keys must be a subset of resource original fields
        # Note : Sort keys are not required to be a subset of
        #        requested output columns/fields
        if self.sort_key:
            if not set(self.sort_key).issubset(set(self.column)):
                print("Specified sort key(s) list {0} must be a subset"
                      "of the resource field's list {1}".format(self.sort_key,
                                                                self.column))
                sys.exit(0)

        # Get the output formatter type(e.g. csv, html and table)
        self.formatter = argparse.get('formatter')
#        # Except the list commands
        if not self.formatter:
            self.formatter = 'table'

        # Holds HTTP Response
        self.response = None

    def create(self, attributes):
        """Handle the create commands.

        Also prints the HTTP response in requested format

        Args:
            attributes (dict): HTTP Body

        Returns:
            None
        """
#        pdb.set_trace()
        self.http_request['method'] = 'POST'
        # Convert the attributes dict. to JSON
        self.http_request['data'] = json.dumps(attributes)

        # Send HTTP request
        self.response = HTTPClient.send_request(**self.http_request)

        # If HTTP Status Code is 201, print the response
        if self.response.status_code == http_status_code.CREATED:
            self._print_output(self.response.json())
        else:
            pass
            # TODO: Handle errors for HTTP errors

    def show(self, attributes=None):
        """Handles the show commands.

        Also prints the HTTP response in requested format

        Args:
            attributes (dict): HTTP Body

        Returns:
            None
        """
        self.http_request['method'] = 'GET'
        self.http_request['url'] = (self.http_request['url'] +
                                    attributes.pop('id') + '/')

        # Send HTTP request
        self.response = HTTPClient.send_request(**self.http_request)

        # If HTTP Status Code is 200, print the response
        if self.response.status_code == http_status_code.OK:
            self._print_output(self.response.json())
        else:
            pass
            # TODO: Handle errors for HTTP errors

    def list(self, attributes=None):
        """Handles the list commands.

        Also prints the HTTP response in requested format

        Args:
            attributes (dict): HTTP Body

        Returns:
            None
        """
#        pdb.set_trace()
        self.http_request['method'] = 'GET'
        self.response = HTTPClient.send_request(**self.http_request)

        # If HTTP Status Code is 200, print the response
        if self.response.status_code == http_status_code.OK:
            self._print_output_for_list(self.response.json())
        else:
            pass
            # TODO: Handle errors for HTTP errors

    def update(self, attributes):
        """Handles the update commands.

        Also prints the HTTP response in requested format

        Args:
            attributes (dict): HTTP Body

        Returns:
            None
        """
        self.http_request['method'] = 'PUT'
        self.http_request['url'] = (self.http_request['url'] +
                                    attributes.pop('id') + '/')

        # Convert the attributes dict. to JSON
        self.http_request['data'] = json.dumps(attributes)

        # Send HTTP request
        self.response = HTTPClient.send_request(**self.http_request)

        # If HTTP Status Code is 200, print the response
        if self.response.status_code == http_status_code.OK:
            self._print_output(self.response.json())
        else:
            pass
            # TODO: Handle errors for HTTP errors

    def delete(self, attributes_dict=None):
        """Handles the delete commands.

        Also prints the HTTP response in requested format

        Args:
            attributes_dict (dict): HTTP Body

        Returns:
            None
        """
        self.http_request['method'] = 'DELETE'
        self.http_request['url'] = (self.http_request['url'] +
                                    attributes_dict.pop('id') + '/')

        # Send HTTP request
        self.response = HTTPClient.send_request(**self.http_request)

        # If HTTP Status Code is 204, print the response
        if self.response.status_code == http_status_code.NO_CONTENT:
            print(self.response)
        else:
            pass
            # TODO: Handle errors for HTTP errors

    @staticmethod
    def _handle_http_unsuccessful_response(http_response):

        if http_response.status_code == http_status_code.NOT_FOUND:
            print("NotFound: The resource could not be found. (HTTP 404)")

        elif http_response.staus_code == http_status_code.BAD_REQUEST:
            print ("Error(BadRequest): (HTTP 400)")

    def _print_output(self, http_response):
        """Format the output in the required form

        Args:
            http_response (dict): HTTP Response(JSON)

        Returns:
            None
        """
        self.column = self.column if not self.fields else self.fields

        # Table column names
        field_names = ["Field", "Value"]
#        pdb.set_trace()
        http_response = utils_vpn.integer_to_string_mapping_show(http_response)

        if self.formatter != 'csv':
            # table or html format
            table = PrettyTable(field_names)
            table.align["Field"] = "l"
            for column in self.column:
                row = [column, json.dumps(http_response.get(column, ' '))]
                table.add_row(row)
            self.print_table_or_html(table)
        else:
            # csv format
            wr = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(field_names)
            for column in self.column:
                row = [column, http_response.get(column, ' ')]
                wr.writerow(row)

    def _print_output_for_list(self, records):
        """Format the output in the required form(only for list
        commands)

        Args:
            records (list of dict): HTTP Response(JSON) records

        Returns:
            None
        """
#        pdb.set_trace()
        # Table field names (default is 'id' and 'name' . Else use the
        # requested columns/fields in the commands
        list_column = ['id', 'name'] if not self.fields else self.fields

        # If sort is requested in the commands, sort the response
        if self.sort_key:
            records = self.sort(records)

#        records = utils_vpn.integer_to_string_mapping_list(records)

        if self.formatter != 'csv':
            # table or html format
            table = PrettyTable(list_column)
            for record in records:
                row = [record.get(column, ' ') for column in list_column]
                table.add_row(row)
            self.print_table_or_html(table)
        else:
            # csv format
            wr = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(list_column)
            for record in records:
                row = [record.get(column, ' ') for column in list_column]
                wr.writerow(row)

        # If detail is requested in commands, print detail of each
        # record
        if self.show_details:
            print("\nDetail of each of the above records: \n")
            for record in records:
                self._print_output(record)
                print("\n")

    def sort(self, record):
        """Sort the records per the list of sort_key & sort_direction

        The built-in sorted() function is guaranteed to be stable. So,
        to support sorting on multiple keys, start sorting the list
        with the keys starting with last of the provided keys. Then
        proceed by picking keys towards start of list once at a time.


        Args:
            record (list): list

        Returns:
            Returns the list of sorted records
        """

        # Reverse the order of the sort key list
        if self.sort_key:
            self.sort_key.reverse()
        else:
            return

        len_sort_key = len(self.sort_key)
        len_sort_direction = len(self.sort_direction)

        # Number of sort key(s) and sort direction(s) should be same.

        # If no. of sort key(s) is less than no. of sort direction(s),
        # ignore the extra sort direction by truncating the
        # sort_direction.
        # Else, if no. of sort key(s) is less than no. of sort
        # direction(s), append the sort_direction with 'asc' to make
        # the two lists equal.
        # Note: 'asc' is the default value chosen
        if len_sort_key < len_sort_direction:
            self.sort_direction = self.sort_direction[:len_sort_key]
        elif len_sort_key > len_sort_direction:
            diff_len = len_sort_key - len_sort_direction
            self.sort_direction.extend(['asc'] * diff_len)

        # As done with sort_key, also reverse the sort_direction
        self.sort_direction.reverse()

        for i, _ in enumerate(self.sort_direction):
            if self.sort_direction[i] == 'asc':
                record = sorted(record,
                                key=itemgetter(self.sort_key[i]),
                                reverse=False)

            # If sort_direction is 'desc', set reverse = True
            if self.sort_direction[i] == 'desc':
                record = sorted(record,
                                key=itemgetter(self.sort_key[i]),
                                reverse=True)

        return record

    def print_table_or_html(self, table):
        """Print output in 'table' or 'html' form

        Args:
            table: PrettyTable object

        Returns:
            None
        """
        if self.formatter == 'table':
            print(table)
        elif self.formatter == 'html':
            print(table.get_html_string())
