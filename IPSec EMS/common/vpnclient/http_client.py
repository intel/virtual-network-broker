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

import requests

MAX_URI_LEN = 8192


class HTTPClient(object):
    """Handles the HTTP REST API calls and responses, including
    authentication.
    """

    @staticmethod
    def send_request(**kwargs):
        """Send the HTTP request to server

        Args:
            **kwargs (dict): HTTP request attributes

        Returns:
            response from the server
        """
        try:
            # TODO: Temporarily popped out till auth and https is ready
            kwargs.pop('cert', None)
            kwargs.pop('auth', None)

            response = requests.request(
                method=kwargs.pop('method', None),
                url=kwargs.pop('url', None),
                params=kwargs.pop('params', None),
                data=kwargs.pop('data', None),
                files=kwargs.pop('files', None),
                headers=kwargs.pop('headers', None),
                cookies=kwargs.pop('cookies', None),
                auth=kwargs.pop('auth', None),
                cert=kwargs.pop('cert', None),
                verify=kwargs.pop('verify', None),
                timeout=kwargs.pop('timeout', None),
                **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            print e.__doc__
            print e.message




