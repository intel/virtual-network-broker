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

"""Registration and De-Registration of IPsecEnforcer with IPsec EMS"""

import logging

from django.utils.translation import ugettext as _

from services.api import storage
from services.ipsecenforcer.utils import str_to_dict, consul_key_join
from services.api.serializers.vpn_choices import RESOURCE_TO_RELATION_MAP

LOG = logging.getLogger(__name__)

RELATION_IPSECENFORCER = (
    RESOURCE_TO_RELATION_MAP['IPsecEnforcerRegistration']
)
RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP = (
    RESOURCE_TO_RELATION_MAP['IPsecEnforcerVPNEndpointMap']
)
RELATION_VPNENDPOINT_IPSECENFORCER_FQDN_MAP = (
    RESOURCE_TO_RELATION_MAP['VPNEndpointIPsecEnforcerFQDNMap']
)
RELATION_IPSECENFORCER_CONFIG_VERSION = (
    RESOURCE_TO_RELATION_MAP['IPsecEnforcerConfigVersion']
)


class IPsecEnforcerInfo(object):
    def register_ipsecenforcer(self, record):
        """Register IPsecEnforcer

        Args:
            record (IPsecEnforcerRegistration): IPsecEnforcer
                Registration record
        """
        session_id = storage.plugin.create_session()

        try:
            ipsecenforcer_endpoint_list = (
                self.get_ipsecenforcer_to_vpnendpoint_map(
                        record.id,
                        temp=True)
            )

            for ipsecenforcer_endpoint in ipsecenforcer_endpoint_list:
                self.put_ipsecenforcer_to_vpnendpoint_map(
                        record.id,
                        ipsecenforcer_endpoint)

                # Store the VPNEndpoint and IPsecEnforcer (id & FQDN)
                self.put_vpnendpoint_to_ipsecenforcer_fqdn_map(
                        ipsecenforcer_endpoint['endpoint_id'],
                        record.id,
                        record.fqdn,
                        record.fqdn_tunnel)
        finally:
            storage.plugin.destroy_session(session_id)

        storage.plugin.put_record(RELATION_IPSECENFORCER, record)

        LOG.info(_("Registered IPsecEnforcer( id: %s, fqdn: %s )" %
                   (record.id, record.fqdn)))

    @staticmethod
    def get_ipsecenforcer_info(record):
        """Fetch the IPsecEnforcer information

        Args:
            record:

        Returns:

        """
        return storage.plugin.get_record(RELATION_IPSECENFORCER, record)

    def deregister_ipsecenforcer(self, record):
        """De-Register the IPsecEnforcer

        Args:
            record (IPsecEnforcerRegistration): IPsecEnforcer
                Registration record
        """
        session_id = storage.plugin.create_session()

        try:
            ipsecenforcer_endpoint_list = (
                self.get_ipsecenforcer_to_vpnendpoint_map(
                        record.id)
            )

            for ipsecenforcer_endpoint in ipsecenforcer_endpoint_list:

                # Delete the VPNEndPoint to IPSecEnforcer/FQDN map record
                self.delete_vpnendpoint_to_ipsecenforcer_fqdn_map(
                        ipsecenforcer_endpoint['endpoint_id'],
                        record.fqdn)

                # Delete all the VPNEndpoint(s) associated with IPSecEnforcer
                self.delete_ipsecenforcer_to_vpnendpoint_map(record.id)

                # Delete the config version of IPSecEnforcer
                self.delete_ipsecenforcer_config_version(record.id)

                # Delete the HeartbeatMiss count of IPsecEnforcer record
                HeartbeatMissOfIPsecEnforcer().delete_heartbeat_miss_count(
                        record.id,
                        record.fqdn)

        finally:
            storage.plugin.destroy_session(session_id)

        storage.plugin.delete_record(RELATION_IPSECENFORCER, record)

        LOG.info(_("De-Registered IPsecEnforcer( id: %s, fqdn: %s )" %
                   (record.id, record.fqdn)))

    @staticmethod
    def put_ipsecenforcer_to_vpnendpoint_map(ipsecenforcer_id,
                                             enforcer,
                                             temp=False):
        """Store IPsecEnforcer to VPNEndpoint mapping

        An IPsecEnforcer could belong to multiple VPNEndpoint(s)

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            enforcer (IPsecEnforcerRegistration): IPsecEnforcer
                                                  Registration record
            temp (bool): whether record is temporary or not
        """
        if temp:
            relation_name = consul_key_join(
                    'temp',
                    RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP)
        else:
            relation_name = RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP

        key = consul_key_join(relation_name,
                              ipsecenforcer_id,
                              enforcer['endpoint_id'])

        value = str(enforcer)

        storage.plugin.put_kv(key, value)

    @classmethod
    def get_ipsecenforcer_to_vpnendpoint_map(cls, ipsecenforcer_id, temp=False):
        """Fetch VPNEndpoint list for a given VPNEndpoint mapping

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            temp (bool): whether record is temporary or not

        Returns:
            list:
        """
        if temp:
            relation_name = consul_key_join(
                    'temp',
                    RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP)
        else:
            relation_name = RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP

        key_prefix = consul_key_join(relation_name, ipsecenforcer_id)

        # Retrieve the list of all records from Consul
        # Note : 'recurse=True' option fetches all the record with the
        # given key prefix
        consul_index, data = storage.plugin.connection.kv.get(key_prefix,
                                                              recurse=True)

        if data is None:
            return []

        # Prepare a list of all the records 'Value' field
        records = [str_to_dict(record['Value']) for record in data]

        return records

    @staticmethod
    def delete_ipsecenforcer_to_vpnendpoint_map(ipsecenforcer_id, temp=False):
        """Delete the IPsecEnforcer to VPNEndpoint mapping

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            temp (bool): whether record is temporary or not
        """
        if temp:
            relation_name = consul_key_join(
                    'temp',
                    RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP)
        else:
            relation_name = RELATION_IPSECENFORCER_TO_VPNENDPOINT_MAP

        key_prefix = consul_key_join(relation_name, ipsecenforcer_id)

        storage.plugin.connection.kv.delete(key_prefix, recurse=True)

    @staticmethod
    def put_vpnendpoint_to_ipsecenforcer_fqdn_map(vpnendpoint_id,
                                                  ipsecenforcer_id,
                                                  fqdn,
                                                  fqdn_tunnel):
        """Store the IPsecEnforcer FQDN and the corresponding
         VPNEndpoint mapping

        Args:
            vpnendpoint_id (str): id of VPNEndpoint
            ipsecenforcer_id (str) : id of IPsecEnforcer
            fqdn (str): FQDN of IPsecEnforcer
            fqdn_tunnel (str): FQDN of IPsecEnforcer Tunnel Interface
        """
        key = consul_key_join(
                RELATION_VPNENDPOINT_IPSECENFORCER_FQDN_MAP,
                vpnendpoint_id,
                fqdn)

        value = {
            'ipsecenforcer_id': ipsecenforcer_id,
            'fqdn': fqdn,
            'fqdn_tunnel': fqdn_tunnel
        }

        value = str(value)

        storage.plugin.put_kv(key, value)

        LOG.info(_("Stored map of VPNEndpoint %s with IPsecEnforcer id %s and"
                   "FQDN %s" % (vpnendpoint_id, ipsecenforcer_id, fqdn)))

    @staticmethod
    def get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(vpnendpoint_id):
        """Fetch IPsecEnforcer FQDN list for a given VPNEndpoint

        Args:
            vpnendpoint_id (str): id of VPNEndpoint

        Returns:
            Empty List ([]) OR List of records
        """
        key_prefix = consul_key_join(
                RELATION_VPNENDPOINT_IPSECENFORCER_FQDN_MAP,
                vpnendpoint_id)

        # Retrieve the list of all records from Consul
        # Note : 'recurse=True' option fetches all the record with the
        # given key prefix
        consul_index, data = storage.plugin.connection.kv.get(key_prefix,
                                                              recurse=True)

        if data is None:
            return []

        # Prepare a list of all the records 'Value' field
        records = [str_to_dict(record['Value']) for record in data]

        LOG.debug(_("Fetched map of VPNEndpoint %s with IPsecEnforcer id & "
                    "FQDN" % vpnendpoint_id))
        return records

    @staticmethod
    def delete_vpnendpoint_to_ipsecenforcer_fqdn_map(vpnendpoint_id, fqdn):
        """Delete the IPsecEnforcer FQDN and the corresponding
         VPNEndpoint mapping

        Args:
            vpnendpoint_id (str): id of VPNEndpoint
            fqdn (str): FQDN of IPsecEnforcer
        """
        key = consul_key_join(RELATION_VPNENDPOINT_IPSECENFORCER_FQDN_MAP,
                              vpnendpoint_id,
                              fqdn)

        storage.plugin.delete_kv(key)

        LOG.info(_("Deleted map of VPNEndpoint %s with IPsecEnforcer FQDN %s" %
                   (vpnendpoint_id, fqdn)))

    def increment_ipsecenforcer_config_version(self, ipsecenforcer_id):
        """Store the IPsecEnforcer FQDN and the corresponding
         VPNEndpoint mapping

        Args:
            ipsecenforcer_id (str) : id of IPsecEnforcer

        Returns:
            str : version number of IPsecEnforcer config
        """
        key = consul_key_join(RELATION_IPSECENFORCER_CONFIG_VERSION,
                              ipsecenforcer_id)

        session_id = storage.plugin.create_session()
        try:
            config_version = self._get_ipsecenforcer_config_version(
                    ipsecenforcer_id)

            # Always increment the config version by 1
            if config_version is None:
                config_version = 1
            else:
                config_version = int(config_version) + 1

            storage.plugin.put_kv(key, str(config_version))

        finally:
            storage.plugin.destroy_session(session_id)

        LOG.info(_("Incremented config version of IPsecEnforcer id %s "
                   "and config version %s" % (ipsecenforcer_id, config_version)
                   ))

        return config_version

    @staticmethod
    def _get_ipsecenforcer_config_version(ipsecenforcer_id):
        """Fetch IPsecEnforcer FQDN list for a given VPNEndpoint

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer

        Returns:
            str : version number of IPsecEnforcer config
            None : if no config version exists
        """
        key = consul_key_join(RELATION_IPSECENFORCER_CONFIG_VERSION,
                              ipsecenforcer_id)

        config_version = storage.plugin.get_kv(key)

        if config_version is None:
            LOG.debug(_("Fetched config version of IPsecEnforcer id %s with "
                        "value 'None'" % ipsecenforcer_id))
        else:
            LOG.debug(_("Fetched config version of IPsecEnforcer id %s with "
                        "value %s" % (ipsecenforcer_id, config_version)))

        return config_version

    @staticmethod
    def delete_ipsecenforcer_config_version(ipsecenforcer_id):
        """Delete the IPsecEnforcer FQDN and the corresponding
         VPNEndpoint mapping

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
        """
        key = consul_key_join(RELATION_IPSECENFORCER_CONFIG_VERSION,
                              ipsecenforcer_id)

        LOG.info(_("Deleted config version of IPsecEnforcer id %s" %
                   ipsecenforcer_id))

        storage.plugin.delete_kv(key)


class HeartbeatMissOfIPsecEnforcer(object):
    """Store the Heartbeat miss count for an IPsecEnforcer"""

    relation = 'heartbeat_miss_ipsecenforcer'

    @classmethod
    def put_heartbeat_miss_count(cls, ipsecenforcer_id, fqdn, count):
        """Store the Heartbeat Miss record for IPsecEnforcer

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            fqdn (str): FQDN of IPsecEnforcer
            count (int): Heartbeat Miss count
        """
        key = consul_key_join(cls.relation, ipsecenforcer_id, fqdn)

        value = str(count)

        storage.plugin.put_kv(key, value)

        LOG.info(_("Stored Heartbeat Miss count of IPsecEnforcer id %s with "
                   "FQDN %s" % (ipsecenforcer_id, fqdn)))

    @classmethod
    def get_heartbeat_miss_count(cls, ipsecenforcer_id, fqdn):
        """Fetch the Heartbeat Miss count for IPsecEnforcer

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            fqdn (str): FQDN of IPsecEnforcer

        Returns:
            int: Heartbeat Miss count of IPsecEnforcer
        """
        key = consul_key_join(cls.relation, ipsecenforcer_id, fqdn)

        # Fetch the Heartbeat Backoff Count
        count = storage.plugin.get_kv(key)

        if count is None:
            return 0

        LOG.debug(_("Fetched Heartbeat Miss count %s of IPsecEnforcer id %s "
                    "with FQDN %s" % (count, ipsecenforcer_id, fqdn)))

        return int(count)

    @classmethod
    def delete_heartbeat_miss_count(cls, ipsecenforcer_id, fqdn):
        """Delete the Heartbeat Miss record for IPsecEnforcer

        Args:
            ipsecenforcer_id (str): id of IPsecEnforcer
            fqdn (str): FQDN of IPsecEnforcer
        """
        key = consul_key_join(cls.relation, ipsecenforcer_id, fqdn)

        LOG.info(_("Deleted Heartbeat Miss record of IPsecEnforcer id %s with "
                   "FQDN %s" % (ipsecenforcer_id, fqdn)))

        storage.plugin.delete_kv(key)