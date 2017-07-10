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

import logging
import os
import subprocess
import unittest


import sys




class TestPost(unittest.TestCase):

    def setUp(self):
        my_env = os.environ.copy()
        my_env['IPSEC_EMS_FQDN']='10.1.68.38'
        my_env['IPSEC_EMS_AUTH_STRATEGY']='token'
        my_env['IPSEC_EMS_AUTH_TOKEN']='1qa5rfefgrtwu73wiu3'
        my_env['IPSEC_EMS_CERT']='/root/client.cert'
        my_env['IPSEC_EMS_KEY']='/root/client.key'
        self.env = my_env

    def test_try(self):
        p = subprocess.Popen(["python", "/root/common_vpn/dcg_netwrorksecurity-ipsec_ems/common/vpnclient/shell.py",
                               "vpn-endpointgroup-create", "group1"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=self.env)
        output, err = p.communicate()
        print(output)
        #print(err)

if __name__ == '__main__':
    unittest.main()
