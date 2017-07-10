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
import os
import socket
import logging
import json

logging.basicConfig(filename="/var/log/cred-service-prov.log",
                    filemode="w", level=logging.INFO)

## Placeholder for parameters ##


class CloudInitAgent:

    """
    Class handling the provisioning of the app specific
    secret and config material
    """

    def __init__(self, url, token, scope_name,
                 certs_path, config_path, conf_filename):
        self.url = url
        self.token = token
        self.scope_name = scope_name
        self.certs_path = certs_path
        self.config_path = config_path
        self.conf_filename = conf_filename
        self.cert_url = self.url + self.scope_name + "/certificate/"

    def write_cert_to_file(self, certs_obj, cert_elem, cert_ext):
        """Helper method to write a given certificate material to a specified
           certificate file.

        Args:
            certs_obj (dict): Contains various Certificate objects
                              Public/Private Key & Issuing CA Cert
            cert_elem (str): Specicies the element of interest in the
                             certs_obj
            cert_ext (type): File extension used to save the cert element

        Returns:
            None
        """

        filename = self.certs_path + cert_elem + '.' + cert_ext
        Utils.create_parent_folders(filename)
        Utils.write_to_file(filename, certs_obj['response'][cert_elem])

    def read_cert_from_file(self, cert_elem):
        """Helper method to write a given certificate material to a specified
           certificate file.

        Args:
            certs_obj (dict): Contains various Certificate objects
                              Public/Private Key & Issuing CA Cert
            cert_elem (str): Specicies the element of interest in the
                             certs_obj

        Returns:
            cert in pem
        """

        filename = self.certs_path + cert_elem
        if os.path.exists(os.path.dirname(filename)):
            file_handle = open(filename, 'r')
            return file_handle.read()

    def issue_certificates(self, crt_common_name):
        """Core method which retrieves the certificate and other secret
           material using the temp token provided

        Args:
            crt_common_name (str): Common name of the requesting Certificate

        Returns:
            None
        """

        try:
            logging.info("Requesting TLS Certificate from %s for user %s"
                         % (self.scope_name, crt_common_name))
            data = {'common_name': crt_common_name}
            headers = {'X-Auth-Token': self.token}
            response = requests.post(self.cert_url, data=data, headers=headers)
            pki_certs = response.json()
            self.write_cert_to_file(pki_certs, 'certificate', 'crt')
            self.write_cert_to_file(pki_certs, 'issuing_ca', 'crt')
            self.write_cert_to_file(pki_certs, 'private_key', 'pem')
            logging.info("Certificates successfully issued for user %s" % crt_common_name)
        except Exception, e:
            logging.warning(e)
            error = "Error retrieving the certificates with the Temp token provided"
            logging.error(error)
            raise Exception(error)

    def sign_certificates(self, crt_common_name, csr_filename):
        """Core method which retrieves the certificate and other secret
           material using the temp token provided

        Args:
            crt_common_name (str): Common name of the requesting Certificate

        Returns:
            None
        """

        try:
            logging.info("Requesting TLS Certificate from %s for user %s"
                         % (self.scope_name, crt_common_name))
            csr = self.read_cert_from_file(csr_filename)
            data = {'common_name': crt_common_name, 'csr': csr}
            headers = {'X-Auth-Token': self.token}
            response = requests.post(self.cert_url, data=data, headers=headers)
            pki_certs = response.json()
            self.write_cert_to_file(pki_certs, 'certificate', 'crt')
            logging.info("Certificate successfully signed for user %s" % crt_common_name)
        except Exception, e:
            logging.warning(e)
            error = "Error retrieving the certificates with the Temp token provided"
            logging.error(error)
            raise Exception(error)


class Utils:

    """
    Utilities class for helper methods
    """

    def __init__(self):
        self.hey = "132"

    @staticmethod
    def create_parent_folders(filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

    @staticmethod
    def write_to_file(filename,data):
        file_handle = open(filename, 'w')
        file_handle.write(data)
        file_handle.close()


cname = socket.getfqdn()

# These should be configured per scope
cert_path = '/etc/cred_service/certs/'
conf_path = '/etc/cred_service/conf/'
conf_filename = 'application_settings.conf'
csr_filename = 'certificate_request.csr'

agent = CloudInitAgent(url, ttoken, scope, cert_path, conf_path, conf_filename)
agent.issue_certificates(cname)
#agent.sign_certificates(cname, csr_filename)
