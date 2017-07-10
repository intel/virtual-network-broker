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

import copy
import itertools
import logging
from string import lower

from django.utils.translation import ugettext as _

from services.api import storage
from services.api.serializers.utils_serializers import (
    get_vpnendpoints_field, get_vpnendpoints_resource
)
from services.api.serializers.vpn_choices import (
    RESOURCE_TO_RELATION_MAP,
    VPN_BIND_GROUP, VPN_BIND_LOCALSITE, VPN_BIND_REMOTESITE
)
from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo
from services.ipsecenforcer.utils import (
    generate_psk_string)

LOG = logging.getLogger(__name__)


class IPsecEnforcerConfig(object):

    def __init__(self):
        # Format of configuration policy for IPsecEnforcer
        self.ipsecenforcer_config = dict(ikepolicy={},
                                         ipsecpolicy={},
                                         vpnbind_group_to_group={},
                                         vpnbind_group_to_localsite={},
                                         vpnbind_group_to_remotesite={},
                                         vpnbind_localsite_to_localsite={},
                                         vpnbind_localsite_to_remotesite={},
                                         vpnendpointgroup={},
                                         vpnendpointlocalsite={},
                                         vpnendpointremotesite={},
                                         fqdn_list={},
                                         fqdn_pair_psk={},
                                         vpncertificate={},
                                         vpncacertificate={},
                                        )

    @staticmethod
    def _pop_unrequired_fields(record):
        """Remove unrequired fields from record

        These fields are not required for policy configuration at
        IPsecEnforcer

        Args:
            record (dict): record with fields

        Returns:
            str : record with unrequired fields
        """
        unrequired_fields = ('name', 'description')
        for field in unrequired_fields:
            record.pop(field, None)

    def _add_config_version(self, ipsecenforcer_id):
        """Add config version

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
        """
        config_version = (
            IPsecEnforcerInfo().increment_ipsecenforcer_config_version(
                ipsecenforcer_id)
        )

        self.ipsecenforcer_config.update({'version': config_version})

    def _add_ikepolicy(self, ikepolicy_id):
        """Add IKEPolicy to the configuration policy

        Args:
            ikepolicy_id (str): id of IKEPolicy
        """
        ikepolicy = storage.plugin.get_record('ikepolicies', ikepolicy_id)
        assert (ikepolicy is not None)

        _id = ikepolicy.pop('id')
        self._pop_unrequired_fields(ikepolicy)
        self.ipsecenforcer_config['ikepolicy'].update({_id: ikepolicy})

    def _add_ipsecpolicy(self, ipsecpolicy_id):
        """Add IPsecPolicy to the configuration policy

        Args:
           ipsecpolicy_id (str): id of IPsecPolicy
        """
        ipsecpolicy = storage.plugin.get_record('ipsecpolicies', ipsecpolicy_id)
        assert (ipsecpolicy is not None)

        _id = ipsecpolicy.pop('id')
        self._pop_unrequired_fields(ipsecpolicy)
        self.ipsecenforcer_config['ipsecpolicy'].update({_id: ipsecpolicy})

    def _add_vpnbind(self, vpnbind_type, vpnbind_record):
        """Add VPNBind record to the configuration policy

        Args:
            vpnbind_type (str): Type of VPNBind record
            vpnbind_record (dict): id of IPsecPolicy
        """
        bind_record = copy.deepcopy(vpnbind_record)
        assert (bind_record is not None)

        _id = bind_record['id']
        self._pop_unrequired_fields(bind_record)
        self.ipsecenforcer_config[vpnbind_type].update({_id: bind_record})

    def _add_vpnendpoint(self, vpnbind_record, vpnendpoint_resource,
                         vpnendpoint_field):
        """Add endpoint to the configuration policy

        Args:
            vpnbind_record (dict): VPNBind record
            vpnendpoint_resource (str): Type of VPNEndpoint resource
            vpnendpoint_field (str): VPNEndpoint field name in VPNBind
                record
        """
        vpnendpoint_record = storage.plugin.get_record(
                RESOURCE_TO_RELATION_MAP[vpnendpoint_resource],
                vpnbind_record[vpnendpoint_field])

        _id = vpnendpoint_record.pop('id')
        self._pop_unrequired_fields(vpnendpoint_record)

        self.ipsecenforcer_config[lower(vpnendpoint_resource)].update(
                {_id: vpnendpoint_record})

        if vpnbind_record['auth_mode'] == 'cert':
            self._add_vpncertificate(vpnendpoint_record['vpncertificate_id'])

    def _add_vpncertificate(self, vpncertificate_id):
        """Add VPNCertificate to the configuration policy

        Args:
            vpncertificate_id (str): id of VPNCertificate
        """
        vpncertificate = storage.plugin.get_record(
                RESOURCE_TO_RELATION_MAP['VPNCertificate'],
                vpncertificate_id)

        _id = vpncertificate.pop('id')
        self._pop_unrequired_fields(vpncertificate)
        self.ipsecenforcer_config['vpncertificate'].update(
                {_id: vpncertificate})

        self._add_vpncacertificate(vpncertificate['vpncacertificate_id'])

    def _add_vpncacertificate(self, vpncacertificate_id):
        """Add VPNCACertificate to the configuration policy

        Args:
            vpncacertificate_id (str): id of VPNCACertificate
        """
        vpncacertificate = storage.plugin.get_record(
                RESOURCE_TO_RELATION_MAP['VPNCACertificate'],
                vpncacertificate_id)

        _id = vpncacertificate.pop('id')
        self._pop_unrequired_fields(vpncacertificate)
        self.ipsecenforcer_config['vpncacertificate'].update(
                {_id: vpncacertificate})

    def _add_fqdn_list_of_vpnendpoint(self, vpnendpoint_id):
        """Add FQDN of Peer VPNEndpoint to the configuration policy

        Args:
            vpnendpoint_id (str): id of VPNEndpointgroup

        Returns:
            list : List of FQDN for VPNEndpoint
        """
        records = (
            IPsecEnforcerInfo().get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(
                    vpnendpoint_id)
        )

        fqdn_list = [record['fqdn_tunnel'] for record in records]

        if fqdn_list:
            self.ipsecenforcer_config['fqdn_list'].update(
                    {vpnendpoint_id: fqdn_list})

        return fqdn_list

    def _add_psk(self, vpnbind_id, psk, peer_vpnendpoint_id, fqdn, peer):
        """Add PSK(Pre-Shared Key)

        Args:
            vpnbind_id (str): id of VPNBind record
            psk (str): PSK provided with the VPNBind record
            peer_vpnendpoint_id (str): id of peer VPNEndpoint
            fqdn (str): FQDN of IPsecEnforcer Tunnel Interface
            peer (bool): True, If IPsecEnforcer belongs to peer
                VPNEndpoint or Else False.
        """
        records = (
            IPsecEnforcerInfo().get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(
                peer_vpnendpoint_id)
        )

        fqdn_list = [record['fqdn_tunnel'] for record in records]

        if peer:
            fqdn_pairs = itertools.product([fqdn], fqdn_list)
        else:
            fqdn_pairs = itertools.product(fqdn_list, [fqdn])

        fqdn_pair_with_psk = self._generate_psk(vpnbind_id,
                                                fqdn_pairs,
                                                psk)

        self.ipsecenforcer_config['fqdn_pair_psk'].update(fqdn_pair_with_psk)

    @staticmethod
    def _generate_psk(vpnbind_id, fqdn_pairs, psk):
        """Generate the PSKs

        Args:
            vpnbind_id (str): id of VPNBind record
            fqdn_pairs (generator): FQDN pairs of IPsecEnforcer and
                peer IPsecEnforcer(s) FQDN
            psk (str): PSK provided for the VPNBind record

        Returns:
            dict : fqdn pair with generated or provided PSK
        """
        fqdn_pair_with_psk = {}
        for pair in fqdn_pairs:
            dict_key = vpnbind_id + '_' + pair[0] + '_' + pair[1]
            if psk:
                fqdn_pair_with_psk.update({dict_key: psk})
            else:
                key = ('fqdn_pair_psk' + '/' + vpnbind_id + '/' + pair[0] +
                       '/' + pair[1])

                stored_psk = storage.plugin.get_kv(key)

                # If PSK is provided, use the provided the PSK. Else generate
                # the PSK for each FQDN PSK.
                if stored_psk:
                    fqdn_pair_with_psk.update({dict_key: stored_psk})
                else:
                    generated_psk = generate_psk_string()
                    storage.plugin.put_kv(key, generated_psk)
                    fqdn_pair_with_psk.update({dict_key: generated_psk})

        return fqdn_pair_with_psk

    def _add_configurations(self, vpnbind_relation, vpnbind_record,
                            vpnendpoint, peer_vpnendpoint):
        """Add all the configurations to the configuration policy

        Args:
            vpnbind_relation (str): name of VPNBind relation
            vpnbind_record (dict): VPNBind record
            vpnendpoint (str):
            peer_vpnendpoint (str):
        """
        self._add_ikepolicy(vpnbind_record['ikepolicy_id'])
        self._add_ipsecpolicy(vpnbind_record['ipsecpolicy_id'])
        self._add_vpnbind(vpnbind_relation, vpnbind_record)

        vpnendpoint_resource, peer_vpnendpoint_resource = (
            get_vpnendpoints_resource(vpnbind_relation))

        self._add_vpnendpoint(vpnbind_record,
                              vpnendpoint_resource,
                              vpnendpoint)

        self._add_vpnendpoint(vpnbind_record,
                              peer_vpnendpoint_resource,
                              peer_vpnendpoint)

    def process_vpnbind_config(self, ipsecenforcer_record,
                               vpnbind_type_resources, vpnendpoint_id):
        """Process the VPN configurations for IPsecEnforcer

        Args:
            ipsecenforcer_record (dict): IPsecEnforcer record
            vpnbind_type_resources(list): VPNBind resources of IPsecEnforcer
                record
            vpnendpoint_id(str): id of VPNEndpoint for IPsecEnforcer
        """
        for resource in vpnbind_type_resources:

            relation = RESOURCE_TO_RELATION_MAP[resource]
            vpnbind_records = storage.plugin.get_records(relation)

            for vpnbind_record in vpnbind_records:

                vpnendpoint_field, peer_vpnendpoint_field = (
                    get_vpnendpoints_field(relation)
                )

                if vpnbind_record[vpnendpoint_field] == vpnendpoint_id:

                    fqdn_list = self._add_fqdn_list_of_vpnendpoint(
                            vpnbind_record[peer_vpnendpoint_field])

                    # Don't proceed and add configurations if there are no peer
                    # IPsecEnforcers
                    if not fqdn_list:
                        continue

                    vpnbind_record.update({"peer": False})

                    self._add_configurations(relation,
                                             vpnbind_record,
                                             vpnendpoint_field,
                                             peer_vpnendpoint_field)

                    if vpnbind_record['auth_mode'] == 'psk':
                        self._add_psk(vpnbind_record['id'],
                                      vpnbind_record['psk'],
                                      vpnbind_record[peer_vpnendpoint_field],
                                      ipsecenforcer_record['fqdn_tunnel'],
                                      peer=True)

                elif vpnbind_record[peer_vpnendpoint_field] == vpnendpoint_id:

                    fqdn_list = self._add_fqdn_list_of_vpnendpoint(
                            vpnbind_record[vpnendpoint_field])

                    # Don't proceed and add configurations if there are no peer
                    # IPsecEnforcers
                    if not fqdn_list:
                        continue

                    vpnbind_record.update({"peer": True})
                    self._add_configurations(relation,
                                             vpnbind_record,
                                             vpnendpoint_field,
                                             peer_vpnendpoint_field)

                    if vpnbind_record['auth_mode'] == 'psk':
                        self._add_psk(vpnbind_record['id'],
                                      vpnbind_record['psk'],
                                      vpnbind_record[vpnendpoint_field],
                                      ipsecenforcer_record['fqdn_tunnel'],
                                      peer=False)

    def prepare_ipsec_enforcer_config(self, ipsecenforcer_id):
        """Prepare VPN configuration for IPsecEnforcer

        Args:
            ipsecenforcer_id (str) : id of IPsecEnforcer

        Returns:
            dict : IPsecEnforcer VPN Configuration
        """
        # Reset the ipsecenforcer_config
        for key in self.ipsecenforcer_config.iterkeys():
            self.ipsecenforcer_config[key].clear()

        # Fetch the IPsecEnforcer record
        ipsec_enforcer_record = storage.plugin.get_record(
                'ipsec_enforcer_registrations',
                ipsecenforcer_id)

        # Fetch the VPNEndpoint(s) corresponding to the IPsecEnforcer
        mapping_records = (
            IPsecEnforcerInfo.get_ipsecenforcer_to_vpnendpoint_map(
                    ipsecenforcer_id)
        )

        for mapping_record in mapping_records:

            if mapping_record['endpoint_type'] == 'group':

                LOG.debug(_("Preparing VPN configurations for IPsecEnforcer id "
                            "%(ipsecenforcer_id)s with vpnendpointgroup id "
                            "%(vpnendpoint_id)s") %
                          {
                              'ipsecenforcer_id': ipsecenforcer_id,
                              'vpnendpoint_id': mapping_record['endpoint_id']
                          }
                          )

                endpoint_record = storage.plugin.get_record(
                        RESOURCE_TO_RELATION_MAP['VPNEndpointGroup'],
                        mapping_record['endpoint_id'])

                self.process_vpnbind_config(ipsec_enforcer_record,
                                            VPN_BIND_GROUP,
                                            endpoint_record['id'])

            elif mapping_record['endpoint_type'] == 'localsite':

                LOG.debug(_("Preparing VPN configurations for IPsecEnforcer id "
                            "%(ipsecenforcer_id)s with vpnendpointlocalsite id "
                            "%(vpnendpoint_id)s") %
                          {
                              'ipsecenforcer_id': ipsecenforcer_id,
                              'vpnendpoint_id': mapping_record['endpoint_id']
                          }
                          )

                endpoint_record = storage.plugin.get_record(
                        RESOURCE_TO_RELATION_MAP['VPNEndpointLocalSite'],
                        mapping_record['endpoint_id'])

                self.process_vpnbind_config(ipsec_enforcer_record,
                                            VPN_BIND_LOCALSITE,
                                            endpoint_record['id'])

            elif mapping_record['endpoint_type'] == 'remotesite':

                LOG.debug(_("Preparing VPN configurations for IPsecEnforcer id "
                            "%(ipsecenforcer_id)s with vpnendpointremotesite "
                            "id %(vpnendpoint_id)s") %
                          {
                              'ipsecenforcer_id': ipsecenforcer_id,
                              'vpnendpoint_id': mapping_record['endpoint_id']
                          }
                          )

                endpoint_record = storage.plugin.get_record(
                        RESOURCE_TO_RELATION_MAP['VPNEndpointRemoteSite'],
                        mapping_record['endpoint_id'])

                self.process_vpnbind_config(ipsec_enforcer_record,
                                            VPN_BIND_REMOTESITE,
                                            endpoint_record['id'])

        if mapping_records:
            self._add_config_version(ipsecenforcer_id)

        return self.ipsecenforcer_config
