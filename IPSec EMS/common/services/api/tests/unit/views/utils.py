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

import tempfile

from rest_framework.test import APITestCase, APIClient

from services.api.serializers.serializers_ikepolicy import IKEPolicy
from services.api.serializers.serializers_ipsecpolicy import IPsecPolicy
from services.api.serializers.serializers_vpncacertificate import (
    VPNCACertificate
)
from services.api.serializers.serializers_vpncertificate import VPNCertificate
from services.api.serializers.serializers_vpnendpointgroup import \
    VPNEndpointGroup
from services.api.serializers.serializers_vpnendpointlocalsite import \
    VPNEndpointLocalSite
from services.api.serializers.serializers_vpnendpointremotesite import \
    VPNEndpointRemoteSite
from services.api.serializers.utils_serializers import generate_uuid
from services.api.tests.unit.views.common import COMMON_URL_PREFIX


class TempIKEPolicy(object):

    def __init__(self):
        self.id = generate_uuid()

    def create(self):
        data = {
            'id': self.id,
            'name': 'ikepolicy1',
            'description': 'myikepolicy1',
            'ike_version': 'v1',
            'encryption_algorithm': ['aes128'],
            'integrity_algorithm': ['sha1'],
            'dh_group': ['modp1536'],
            'phase1_negotiation_mode': 'main',
            'lifetime_value': 3600,
            'lifetime_units': 'seconds',
            'rekey': 'yes',
            'reauth': 'yes',
        }
        IKEPolicy(**data).save()

    def delete(self):
        IKEPolicy.get(id=self.id).delete()


class TempIPsecPolicy(object):

    def __init__(self):
        self.id = generate_uuid()

    def create(self):
        data = {
            'id': self.id,
            'name': 'ipsecpolicy',
            'description': 'myipsecpolicy1',
            'transform_protocol': 'ah',
            'encryption_algorithm': ['aes256'],
            'integrity_algorithm': ['sha1'],
            'dh_group': ['modp1536'],
            'encapsulation_mode': 'transport',
            'lifetime_value': 3600,
            'lifetime_units': 'seconds',
        }
        IPsecPolicy(**data).save()

    def delete(self):
        IPsecPolicy.get(id=self.id).delete()


class TempVPNEndpointGroup(object):

    def __init__(self):
        self.id = generate_uuid()

    def create(self):
        data = {
            'id': self.id,
            'name': 'temp_vpnendpointgroup1'
        }
        VPNEndpointGroup(**data).save()

    def delete(self):
        VPNEndpointGroup.get(id=self.id).delete()


class TempVPNEndpointLocalSite(APITestCase):

    def __init__(self):
        self.client = APIClient()
        self._url = COMMON_URL_PREFIX + "vpnendpointlocalsites/"

    def create(self):
        data = {'name': 'temp_vpnendpointlocalsite1'}
        data.update({'id': self._id})
        response = self.client.post(self._url, data, format='json')
        self._id = response.data.pop('id')

    def delete(self):
        IKEPolicy.get(id=self._id).delete()


class TempVPNEndpointRemoteSite(APITestCase):

    def __init__(self):
        self.client = APIClient()
        self._url = COMMON_URL_PREFIX + "vpnendpointremotesites/"

    def create(self):
        data = {'name': 'temp_vpnendpointremotesite1'}
        data.update({'id': self._id})
        response = self.client.post(self._url, data, format='json')
        self._id = response.data.pop('id')

    def delete(self):
        IKEPolicy.get(id=self._id).delete()


class Certificates(object):

    def __init__(self):
        self.cacert_id = generate_uuid()  # Generate a ca-cert id
        self.cert_id = generate_uuid()  # Generate a cert id

    def prepare_vpncacertificate(self):
        fp_cacert = self.create_cacertificate()
        fp_cakey = self.create_cakey()
        cacert_data = {
            "name": "cacert123",
            "ca_certificate": fp_cacert,
            "ca_key": fp_cakey
        }
        cacert_data.update({"id": self.cacert_id})
        VPNCACertificate(**cacert_data).save()

    def delete_vpncacertificate(self):
        VPNCACertificate.get(id=self.cacert_id).delete()

    def prepare_vpncertificate(self):
        fp_cert = tempfile.TemporaryFile()
        fp_cert.write(b'cert!')
        fp_cert.seek(0)
        fp_key = tempfile.TemporaryFile()
        fp_key.write(b'key!')
        fp_key.seek(0)
        cert_data = {
            "name": "cert123",
            "certificate": fp_cert,
            "key": fp_key,
            "right_id": "@xyz@abc.com"
        }

        self.prepare_vpncacertificate()
        cert_data.update({"vpncacertificate_id": self.cacert_id})
        cert_data.update({'id': self.cert_id})
        VPNCertificate(**cert_data).save()

    def delete_vpncertificate(self):
        VPNCertificate.get(id=self.cert_id).delete()
        self.delete_vpncacertificate()

    @staticmethod
    def create_cacertificate():
        fp_cacert = tempfile.TemporaryFile()
        fp_cacert.write(b'ca-cert!')
        fp_cacert.seek(0)
        return fp_cacert

    @staticmethod
    def create_cakey():
        fp_cakey = tempfile.TemporaryFile()
        fp_cakey.write(b'ca-key!')
        fp_cakey.seek(0)
        return fp_cakey


