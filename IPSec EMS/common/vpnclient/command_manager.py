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
from itertools import izip_longest
from operator import itemgetter
from urlparse import urljoin

from prettytable import PrettyTable
from requests.auth import HTTPBasicAuth

from cli_cfg import PORT
from cli_cfg import WEB_PROTOCOL

sys.path.append(os.path.abspath('..'))
from vpnclient.http_client import HTTPClient

URL_SEP = '/'


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
    update :    PATCH
    delete:     DELETE

    It provides three options(csv, html, table) to format the http
    response received from the server.
    """

    def __init__(self, http_resource, http_secondary_resources, argparse,
                 version, cmd_columns, pk_column):
        self.http_request = {}
        # Communication Protocol and Port for communication with EMS
        #service = 'ipsecvpn'
        service = 'auth/projects/project1'
        self.http_resource = http_resource
        self.pk_column = pk_column

        # Multiple HTTP resources are joined by '_'
        self.http_secondary_resources = http_secondary_resources

        # Default Headers
        self.http_request['headers'] = {
            'User-Agent': 'ipsec-ems-client',
            #'Content-type': 'application/x-www-form-urlencoded'
            'Content-type': 'application/json'
        }

        # REST API Version
        self._version = 'v' + str(int(float(version)))

        # Domain or Namespace of EMS
        self._namespace = argparse.get('namespace')

        # Construct the URL using api version(e.g. v1), namespace, service type
        # and resource type.
        # e.g. https://ems.com:443/v1/main/ipsecvpn/policy
        self._base_url = \
            '{0}://{1}:{2}/{3}/{4}/{5}/'.format(WEB_PROTOCOL.lower(),
                                                argparse.get('ipsec_ems_fqdn'),
                                                PORT,
                                                self._version,
                                                self._namespace,
                                                service)

        self.http_request['url'] = self._base_url + self.http_resource + URL_SEP

        # Header Authentication token OR username:password
        if argparse.get('auth_strategy') is 'token':

            self.http_request['headers'] = (
                {
                    'Authorization': 'Token ' + argparse.get('token')
                }
            )
        elif argparse.get('auth_strategy') is 'credential':
            self._username = argparse.get('username')
            self._password = argparse.get('password')
            self.http_request['auth'] = HTTPBasicAuth(self._username,
                                                      self._password)

        # HTTPS certificate and private key(optional if certificate
        # already contains the key)
        if argparse.get('key'):
            self.http_request['cert'] = (argparse.get('cert'),
                                         argparse.get('key'))
        else:
            self.http_request['cert'] = argparse.get('cert')

        # Verifying certificate with CA
        if argparse.get('cacert'):
            self.http_request['verify'] = argparse.get('cacert')

        # HTTP request timeout
        if argparse.get('http_timeout'):
            self.http_request['timeout'] = argparse.get('http_timeout')

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

        # List of column/field to on the basis to sort records the output
        self.sort_key = argparse.get('sort_key')

        # Sorting directions(asc or desc) for the above keys
        self.sort_direction = argparse.get('sort_direction')

        # Sort keys must be a subset of resource original fields
        # Note : Sort keys are not required to be a subset of
        #        requested output columns/fields
        if self.sort_key:
            if not set(self.sort_key).issubset(set(self.column)):
                print("Specified sort key(s) list {0} must be a subset of the "
                      "resource field's list {1}".format(self.sort_key,
                                                         self.column))
                sys.exit(0)

        # Get the output formatter type(e.g. csv, html and table)
        self.formatter = argparse.get('formatter')
        # Except the list commands
        if not self.formatter:
            self.formatter = 'table'

        # Holds HTTP Response
        self.response = None

    def _pop_files_attributes(self, attributes):
        """Pop and "*cert" and *key" attributes from record

        Args:
            attributes (dict): resource record

        Returns:
            dict: record with no "*key" attribute
        """
        if self.http_resource not in ('vpncacertificates', 'vpncertificates'):
            return
        files = {}
        for key in attributes.keys():
            if key.endswith("certificate") or key.endswith("key"):
                files.update({key: attributes.pop(key)})
        return files

    def create(self, attributes):
        """Handle the CREATE commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'POST'
        self.http_request['files'] = self._pop_files_attributes(attributes)
        if self.http_request['files']:
            self.http_request['headers'].pop('Content-type', None)
            self.http_request['data'] = attributes
        else:
            self.http_request['data'] = json.dumps(attributes)

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.CREATED)

    def show(self, attributes):
        """Handles the SHOW commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'GET'
        self.http_request['url'] = self._prepare_complete_url(attributes)

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.OK)

    def list(self, attributes):
        """Handles the LIST commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'GET'

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.OK)

    def update(self, attributes):
        """Handles the UPDATE commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'PATCH'
        self.http_request['url'] = self._prepare_complete_url(attributes)
        self.http_request['data'] = json.dumps(attributes)

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.OK)

    def delete(self, attributes):
        """Handles the DELETE commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'DELETE'
        self.http_request['url'] = self._prepare_complete_url(attributes)

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.NO_CONTENT)

    def add(self, attributes):
        """Handles the ADD commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        self.http_request['method'] = 'PUT'
        self.http_request['url'] = self._prepare_complete_url(attributes)
        self.http_request['data'] = json.dumps(attributes)

        self.response = HTTPClient.send_request(**self.http_request)

        self._check_status_and_print_http_response(http_status_code.OK)

    def remove(self, attributes):
        """Handles the REMOVE commands

        Args:
            attributes (dict): HTTP Request attributes
        """
        return self.delete(attributes)

    def _prepare_complete_url(self, attrs=None):
        resource_pk = attrs.pop(self.pk_column, '')
        url = urljoin(self.http_request['url'], resource_pk + URL_SEP)

        for resource in self.http_secondary_resources:
            resource_val = attrs.get(resource, '')
            if resource_val:
                url = urljoin(url, resource + URL_SEP + resource_val + URL_SEP)
            else:
                url = urljoin(url, resource + URL_SEP)

        return url

    def _check_status_and_print_http_response(self, expected_code):
        """Check HTTP Response and if applicable, print HTTP response

        Args:
            expected_code (str):  Expected HTTP response status code
        """
        if self.response is None or not self.response.content:
            return

        if self.response.status_code == expected_code:
            response = self.response.json()
            if isinstance(response, list):
                self._print_output_for_list(response)
            else:
                self._print_output(self.response.json())
        else:
            self._handle_http_unsuccessful_response(self.response)

    @staticmethod
    def _handle_http_unsuccessful_response(http_response):

        if http_response.status_code == http_status_code.NOT_FOUND:
            print("NotFound: The resource could not be found (HTTP 404)")
            return
        elif (http_response.status_code ==
                http_status_code.INTERNAL_SERVER_ERROR):
            print ("Error: Server Error (HTTP 500)")
            return
        elif (http_response.status_code ==
                http_status_code.BAD_REQUEST):
            print ("Error: Bad Request (HTTP 400)")
            print (http_response.text)
            return
        else:
            print ("Error: (HTTP %d)" % http_response.status_code)
            print (http_response.text)
            return

    def _print_output(self, http_response):
        """Print and format the output in the requested form

        Args:
            http_response (dict): HTTP Response(JSON)
        """
        self.column = self.column if not self.fields else self.fields

        # Table column names
        column_names = ["Field", "Value"]

        if self.formatter == 'table':
            # table or html format
            table = PrettyTable(column_names)
            table.align["Field"] = "l"
            table.align["Value"] = "c"
            for column in self.column:
                column_value = http_response.get(column, ' ')
                column_value = self._convert_to_ascii(column_value)
                if isinstance(column_value, list):
                    max_len = 0
                    for i in xrange(len(column_value)):
                        column_value[i] = str(column_value[i])
                        column_len = len(column_value[i])
                        if column_len > max_len:
                            max_len = column_len
                    lst = (value.ljust(max_len) for value in column_value)
                    column_value = '\n'.join(lst) + '\n'
                row = [column, column_value]
                table.add_row(row)
            self._print_table_or_html(table)

    def _convert_to_ascii(self, column_value):
        """Convert the elements to ascii

        Args:
            column_value: HTTP Response(JSON) records

        Returns:
            column_value
        """
        if isinstance(column_value, dict):
            return {self._convert_to_ascii(key): self._convert_to_ascii(
                value)
                    for key, value in column_value.iteritems()}
        elif isinstance(column_value, list):
            return [self._convert_to_ascii(value) for value in column_value]
        elif isinstance(column_value, unicode):
            return column_value.encode('utf-8')
        else:
            return column_value

    def _print_output_for_list(self, records):
        """Format the output in the required form(only for list
        commands)

        Args:
            records (list of dict): HTTP Response(JSON) records
        """
        if not records:
            print("No Records")
            return

        # Table field names (default is 'id' and 'name'). Else use the
        # requested columns/fields in the commands
        list_column = ['id', 'name'] if not self.fields else self.fields

        # If sort is requested in the command
        if self.sort_key:
            records = self._sort_records(records)

        if self.formatter == 'table':
            # table or html format
            table = PrettyTable(list_column)
            for record in records:
                row = [record.get(column, ' ') for column in list_column]
                table.add_row(row)
            self._print_table_or_html(table)

        # If detail is requested in commands, print detail of each
        # record
        if self.show_details:
            print("\nDetail of each of the above records: \n")
            for record in records:
                self._print_output(record)
                print("\n")

    def _print_table_or_html(self, table):
        """Print output in 'table' or 'html' form

        Args:
            table: PrettyTable object
        """
        if self.formatter == 'table':
            print(table)
        elif self.formatter == 'html':
            print(table.get_html_string())

    def _sort_records(self, record):
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
