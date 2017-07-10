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

import os
import itertools
import subprocess

from jinja2 import Environment, FileSystemLoader

_IKE_POLICIES = {}
_IPSEC_POLICIES = {}
_IPSEC_STRONGSWAN_CONNECTIONS = []
_IPSEC_STRONGSWAN_SECRETS = []

_DIALECT_MAP = {
    "bi-directional": "start",
    "response-only": "add",
    "v2": "insist",
    "v1": "never"
}

_DIALECT_LIFETIME_UNITS_MAP = {
    'seconds': 's',
    'minutes': 'm',
    'hours': 'h',
    'days': 'd',
}

policy = None


class StrongSwanIKEPolicy(object):
    """Represents IKEPolicy in Strongswan format"""

    DIALECT_IKE_VERSION_MAP = {
        "v1": "ikev1",
        "v2": "ikev2",
    }

    def __init__(self, **kwargs):

        self.ike_version = (
            self.DIALECT_IKE_VERSION_MAP[kwargs.get('ike_version')]
        )

        encryption_algorithm = '-'.join(kwargs.get('encryption_algorithm'))

        integrity_algorithm = '-'.join(kwargs.get('integrity_algorithm'))

        dh_group = '-'.join(kwargs.get('dh_group'))

        self.ike = '-'.join([encryption_algorithm,
                             integrity_algorithm,
                             dh_group])

        phase1_negotiation_mode = kwargs.get('phase1_negotiation_mode')

        if phase1_negotiation_mode == 'main':
            self.aggressive = 'no'
        else:
            self.aggressive = 'yes'

        lifetime_value = kwargs.get('lifetime_value')

        lifetime_units = (
            _DIALECT_LIFETIME_UNITS_MAP[kwargs.get('lifetime_units')]
        )

        self.ikelifetime = str(lifetime_value) + lifetime_units

        self.rekey = kwargs.get('rekey')

        self.reauth = kwargs.get('reauth')


class StrongSwanIPsecPolicy(object):
    """Represents IPsecPolicy in Strongswan format"""

    def __init__(self, **kwargs):

        encryption_algorithm = '-'.join(kwargs.get('encryption_algorithm'))

        integrity_algorithm = '-'.join(kwargs.get('integrity_algorithm'))

        dh_group = '-'.join(kwargs.get('dh_group'))

        esn_mode = kwargs.get('esn_mode')

        transform_protocol = kwargs.get('transform_protocol')

        if transform_protocol == 'esp':
            self.esp = '-'.join([encryption_algorithm,
                                 integrity_algorithm,
                                 dh_group,
                                 esn_mode])
        else:
            self.ah = '-'.join([encryption_algorithm,
                                integrity_algorithm,
                                dh_group])

        self.type = kwargs.get('encapsulation_mode')

        lifetime_value = kwargs.get('lifetime_value')

        lifetime_units = (
            _DIALECT_LIFETIME_UNITS_MAP[kwargs.get('lifetime_units')]
        )

        self.lifetime = str(lifetime_value) + lifetime_units


class Connection(object):
    """Represents VPNBind in Strongswan format"""

    def __init__(self, vpnbind, fqdn, peer_fqdn, vpnbind_type):
        self.connection_name = vpnbind['id'] + '__' + fqdn + '::' + peer_fqdn
        self.dpdaction = vpnbind['dpd_action']
        self.dpddelay = vpnbind['dpd_interval']
        self.dpdtimeout = vpnbind['dpd_timeout']

        if vpnbind['auth_mode'] == 'psk':
            self.authby = 'psk'

        self.auto = 'route'
        self.ikepolicy = _IKE_POLICIES[vpnbind['ikepolicy_id']]
        self.ipsecpolicy = _IPSEC_POLICIES[vpnbind['ipsecpolicy_id']]
        self.left = fqdn
        self.right = peer_fqdn

        vpnendpoint, peer_vpnendpoint = self.get_vpnendpoints(vpnbind,
                                                              vpnbind_type)

        if vpnbind['auth_mode'] == 'psk':
            self.left_id = vpnbind['id'] + '__' + fqdn
            self.right_id = vpnbind['id'] + '__' + peer_fqdn
        elif vpnbind['auth_mode'] == 'cert':
            self.leftcert = str(vpnendpoint.get('vpncertificate_id')) + '.pem'
            self.left_id = policy.get('vpncertificate').get(
                    vpnendpoint.get('vpncertificate_id')).get('right_id')
            self.right_id = policy.get('vpncertificate').get(
                    peer_vpnendpoint.get('vpncertificate_id')).get('right_id')

        if vpnbind_type == 'vpnbind_localsite_to_localsite':
            self.leftsubnet = vpnendpoint.get('cidrs')[0]
            self.rightsubnet = peer_vpnendpoint.get('cidrs')[0]

        if vpnbind['auth_mode'] == 'psk':
            psk_pair = SecretPSK(vpnbind['id'],
                                 self.left_id,
                                 self.right_id,
                                 fqdn,
                                 peer_fqdn,
                                 vpnbind['peer'])
        elif vpnbind['auth_mode'] == 'cert':
            psk_pair = SecretCert(vpnendpoint,
                                  peer_fqdn)
        _IPSEC_STRONGSWAN_SECRETS.append(psk_pair)

    def get_vpnendpoints(self, vpnbind, vpnbind_type):

        vpnendpoint_type, peer_vpnendpoint_type = (
            self.get_vpnendpoint_type(vpnbind_type))

        vpnendpoint_field, peer_vpnendpoint_field = (
            self.get_vpnendpoints_field(vpnbind_type))

        if not vpnbind['peer']:
            vpnendpoint = policy.get(vpnendpoint_type).get(
                    vpnbind[vpnendpoint_field])
            peer_vpnendpoint = policy.get(peer_vpnendpoint_type).get(
                    vpnbind[peer_vpnendpoint_field])
        else:
            vpnendpoint = policy.get(vpnendpoint_type).get(
                    vpnbind[peer_vpnendpoint_field])
            peer_vpnendpoint = policy.get(peer_vpnendpoint_type).get(
                    vpnbind[vpnendpoint_field])

        return vpnendpoint, peer_vpnendpoint

    @staticmethod
    def get_vpnendpoints_field(vpnbind_relation):
        """Prepare the vpnendpoint_id and peer_vpnendpoint_id field for the
        particular VPNBind relation

        Args:
            vpnbind_relation (str): VPNBIND relation/table name

        Returns:
            vpnendpoint_id and peer_vpnendpoint_id for the VPNBIND relation
        """
        parts = vpnbind_relation.split("_")
        vpnendpoint_id = 'vpnendpoint' + parts[1] + '_id'
        peer_vpnendpoint_id = 'peer_vpnendpoint' + parts[3] + '_id'
        return vpnendpoint_id, peer_vpnendpoint_id

    @staticmethod
    def get_vpnendpoint_type(vpnbind_relation):
        """Prepare the vpnendpoint and peer_vpnendpoint for the
        particular VPNBind relation

        Args:
            vpnbind_relation (str): VPNBIND relation/table name

        Returns:
            vpnendpoint_id and peer_vpnendpoint_id for the VPNBIND relation
        """
        parts = vpnbind_relation.split("_")
        vpnendpoint = 'vpnendpoint' + parts[1]
        peer_vpnendpoint = 'vpnendpoint' + parts[3]
        return vpnendpoint, peer_vpnendpoint


class SecretPSK(object):
    def __init__(self, vpnbind_id, left_id, right_id, fqdn, peer_fqdn,
                 peer=False):
        self.auth_mode = 'psk'
        self.left_id = left_id
        self.right_id = right_id
        if not peer:
            self.psk = policy.get('fqdn_pair_psk').get(
                    vpnbind_id + '_' + fqdn + '_' + peer_fqdn)
        else:
            self.psk = policy.get('fqdn_pair_psk').get(
                    vpnbind_id + '_' + peer_fqdn + '_' + fqdn)


class SecretCert(object):
    def __init__(self, vpnendpoint, peer_fqdn):
        self.auth_mode = 'cert'
        self.peer_fqdn = peer_fqdn
        self.key = str(vpnendpoint.get('vpncertificate_id')) + '.pem'


def add_ikepolicy():
    """Add IKEPolicy to _IPSEC_STRONGSWAN_CONNECTIONS"""
    for _id, ikepolicy in policy['ikepolicy'].iteritems():
        _IKE_POLICIES.update({_id: StrongSwanIKEPolicy(**ikepolicy)})


def add_ipsecpolicy():
    """Add IPsecPolicy to _IPSEC_STRONGSWAN_CONNECTIONS"""
    for _id, ipsecpolicy in policy['ipsecpolicy'].iteritems():
        _IPSEC_POLICIES.update({_id: StrongSwanIPsecPolicy(**ipsecpolicy)})


def process_vpncacertificate():
    """Install CA Certificates"""
    for _id, vpncacertificate in policy['vpncacertificate'].iteritems():
        # Write CA Certificate
        ca_certificate = '/etc/ipsec.d/cacerts/' + str(_id) + '.pem'
        with open(ca_certificate, 'wb+') as f:
            f.write(vpncacertificate['ca_certificate'])


def process_vpncertificate():
    """Install Certificates and Keys"""
    for _id, vpncertificate in policy['vpncertificate'].iteritems():
        # Write Certificate
        certificate = '/etc/ipsec.d/certs/' + str(_id) + '.pem'
        with open(certificate, 'wb+') as f:
            f.write(vpncertificate['certificate'])
        # Write Key
        key = '/etc/ipsec.d/private/' + str(_id) + '.pem'
        with open(key, 'wb+') as f:
            f.write(vpncertificate['key'])


def process_vpnbind_group_group():
    """Add VPNBindGroupToGroup to _IPSEC_STRONGSWAN_CONNECTIONS"""

    # If vpnbind_group_to_group is empty, don't process further
    vpnbind_group_to_group = policy.get('vpnbind_group_to_group', None)
    if vpnbind_group_to_group is None:
        return

    for key, value in vpnbind_group_to_group.iteritems():
        if not value['peer']:
            fqdn_pairs = itertools.product(
                    [fqdn],
                    policy.get('fqdn_list').get(value[
                                                'peer_vpnendpointgroup_id']
                                                )
            )
        else:
            fqdn_pairs = itertools.product(
                    [fqdn],
                    policy.get('fqdn_list').get(value['vpnendpointgroup_id'])
            )
        fqdn_pairs = list((fqdn_pair for fqdn_pair in fqdn_pairs if
                           fqdn_pair[0] != fqdn_pair[1]
                           )
                          )
        for fqdn_pair in fqdn_pairs:
            connection = Connection(value,
                                    fqdn_pair[0],
                                    fqdn_pair[1],
                                    'vpnbind_group_to_group'
                                    )
            _IPSEC_STRONGSWAN_CONNECTIONS.append(connection)


def process_vpnbind_localsite_localsite():
    """Add VPNBindLocalSiteToLocalSite to _IPSEC_STRONGSWAN_CONNECTIONS"""

    # If vpnbind_localsite_to_localsite is empty, don't process further
    vpnbind_localsite_to_localsite = policy.get(
            'vpnbind_localsite_to_localsite', None)
    if vpnbind_localsite_to_localsite is None:
        return

    for key, value in vpnbind_localsite_to_localsite.iteritems():
        if not value['peer']:
            fqdn_pairs = itertools.product(
                    [fqdn],
                    policy.get('fqdn_list').get(
                            value['peer_vpnendpointlocalsite_id']
                    )
            )
        else:
            fqdn_pairs = itertools.product(
                    [fqdn],
                    policy.get('fqdn_list').get(
                            value['vpnendpointlocalsite_id']
                    )
            )
        fqdn_pairs = list((fqdn_pair for fqdn_pair in fqdn_pairs if
                           fqdn_pair[0] != fqdn_pair[1]))
        for fqdn_pair in fqdn_pairs:
            connection = Connection(value,
                                    fqdn_pair[0],
                                    fqdn_pair[1],
                                    'vpnbind_localsite_to_localsite')
            _IPSEC_STRONGSWAN_CONNECTIONS.append(connection)


def install_configurations(config, ipsec_enforcer_fqdn):
    """
    Args:
        config:
        ipsec_enforcer_fqdn:

    Returns:

    """
    global policy
    global fqdn
    policy = config
    fqdn = ipsec_enforcer_fqdn

    process_vpncacertificate()
    process_vpncertificate()
    add_ikepolicy()
    add_ipsecpolicy()

    # Reset _IPSEC_STRONGSWAN_CONNECTIONS & _IPSEC_STRONGSWAN_SECRETS
    del _IPSEC_STRONGSWAN_CONNECTIONS[:]
    del _IPSEC_STRONGSWAN_SECRETS[:]

    # if FQDN list is not empty, then process VPNBind Policies
    if policy.get('fqdn_list'):
        process_vpnbind_group_group()
        process_vpnbind_localsite_localsite()
    render_template()


def render_template():
    """Render the

    Returns:

    """
    jinja_environment = Environment(
            loader=FileSystemLoader('registration'),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
    )
    template = jinja_environment.get_template('ipsec.conf.template')
    strongswan_connections = template.render(
            ipsec_strongswan_connections=_IPSEC_STRONGSWAN_CONNECTIONS)
    template = jinja_environment.get_template('ipsec.secret.template')
    strongswan_psk = template.render(
            ipsec_strongswan_secrets=_IPSEC_STRONGSWAN_SECRETS)

    # Write the Strongswan configurations and secrets
    with open('/etc/ipsec.conf', 'w+') as f:
        f.write(strongswan_connections)
    with open('/etc/ipsec.secrets', 'w+') as f:
        os.chmod('/etc/ipsec.secrets', 0o600)
        f.write(strongswan_psk)

    # Reload the Strongswan configurations and reread the secrets
    subprocess.check_call(["ipsec", "reload"])
    subprocess.check_call(["ipsec", "rereadsecrets"])
