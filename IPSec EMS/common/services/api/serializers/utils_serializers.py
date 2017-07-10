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

from collections import OrderedDict
import itertools
import re

import ast
import ipaddress
import json
import uuid

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.reverse import reverse

from services.api import storage
from services.api.serializers.vpn_choices import (
    RESOURCE_TO_RELATION_MAP, RESOURCE_DEPENDENCY_MAP, VPN_BIND
)
from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo


# Custom Validator Fields
class CustomUUIDField(serializers.UUIDField):
    def to_internal_value(self, value):
        if self.uuid_format == 'hex_verbose':
            return str(value)
        else:
            return getattr(value, self.uuid_format)


class HyperlinkedIdentityField(HyperlinkedIdentityField):
    def to_representation(self, value):
        return reverse('user-device-detail',
                       kwargs={'user_pk': value.owner_id, 'uid': value.uid},
                       request=self.context['request'])


def generate_uuid():
    """Generate a random Version 4(v4) UUID

    Returns:
        str: string format of generated UUID
    """
    # Generate a UUID and convert to a string of hex digits
    return str(uuid.uuid4())


def remove_duplicates_from_list(lst):
    return list(OrderedDict.fromkeys(lst))


def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID.

    Note : version is defaulted to 4

    Args:
        uuid_to_test (str): uuid value in string format
        version (int): version no. of uuid {1, 2, 3, 4}

    Returns:
        `True` if uuid_to_test is a valid UUID, otherwise `False`.
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def str_to_dict(value):
    """Converts a string expression to dict

    Args:
        value (str) :

    Returns:
        dict
    """
    return json.loads(value)


class CustomEncoder(json.JSONEncoder):
    """Extend JSONEncoder to handle set type. Convert set to list"""
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def unicode_to_ascii_dict(value):
    return str_to_dict(json.dumps(value, cls=CustomEncoder))


def check_ipaddress_or_fqdn(value):
    """Validate if value is valid IPv4/IPv6 or valid hostname

    Args:
        value (str): ipaddress or fqdn

    Returns:
        If valid return value

    Raises:
        argparse.ArgumentTypeError: If invalid IPv4/IPv6 or fqdn format
    """
    try:
        ipaddress.ip_address(value)
    except ValueError:
        if not _is_valid_host(value):
            msg = "{0} is not a valid IP Address format".format(ipaddress)
            raise serializers.ValidationError(msg)
    return value


def _is_valid_host(hostname):
    """Validate DNS(FQDN or domain or hostname)

    Args:
        hostname (str): FQDN or domain or hostname

    Returns:
        True : if hostname is valid
        False : if hostname is invalid
    """
    is_valid = re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*"
                        "([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$",
                        hostname)
    return is_valid


def pop_keys(records):
    """Pop "*key" attribute from every record in the list

    Args:
        records (list): list of records

    Returns:
        list: list records with no "*key" attribute
    """
    updated_records = []
    for record in records:
        record = pop_key(record)
        updated_records.append(record)
    return updated_records


def pop_key(record):
    """Pop "*key" attribute from record

    Args:
        record (dict): resource record

    Returns:
        dict: record with no "*key" attribute
    """

    for key in record.keys():
        if key.endswith("key"):
            record.pop(key)
            return record


def check_cidrs(cidrs):
    """Validate cidr(s) or subnet(s)

    Args:
        cidrs (list): Subnet(s) in CIDR format

    Raises:
        serializers.ValidationError: If CIDR's list is empty(None), invalid CIDR
        format or inconsistent versions of CIDR in the list
    """
    if not cidrs:
        raise serializers.ValidationError("CIDR's list is empty")

    # Invalid CIDR format
    msg_subpart = " is not a valid CIDR format"
    cidr_type_list = []
    for cidr in cidrs:

        try:
            cidr_type = type(ipaddress.ip_network(cidr))
        except ValueError:
            msg = cidr + msg_subpart
            raise serializers.ValidationError(msg)

        if cidr_type not in (ipaddress.IPv4Network, ipaddress.IPv6Network):
            msg = cidr + msg_subpart
            raise serializers.ValidationError(msg)

        cidr_type_list.append(cidr_type)

    # Inconsistent versions of CIDR in the list
    check_v4 = all(isinstance(x, ipaddress.IPv4Network) for x in cidr_type_list)

    check_v6 = all(isinstance(x, ipaddress.IPv6Network) for x in cidr_type_list)

    if check_v4 and check_v6:
        raise serializers.ValidationError("All the CIDRs must be of either "
                                          "IPv4 or IPv6 format")


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


def get_vpnendpoints_resource(vpnbind_relation):
    """Prepare the vpnendpoint and peer_vpnendpoint resource type for
    the particular VPNBind relation

    Args:
        vpnbind_relation (str): VPNBIND relation/table name

    Returns:
        vpnendpoint_id and peer_vpnendpoint_id for the VPNBIND relation
    """
    parts = vpnbind_relation.split("_")
    vpnendpoint_resource = 'VPNEndpoint' + parts[1].title()
    peer_vpnendpoint_resource = 'VPNEndpoint' + parts[3].title()
    if parts[1] == 'localsite' and parts[3] == 'localsite':
        return 'VPNEndpointLocalSite', 'VPNEndpointLocalSite'
    return vpnendpoint_resource, peer_vpnendpoint_resource


def check_reference(resource, attrs):
    #
    # Reference check for VPNBind records
    #
    # If a IPsecEnforcer is using a VPNBind record, then the VPNBind should not
    # be allowed to be deleted.
    if resource in VPN_BIND:
        relation = RESOURCE_TO_RELATION_MAP[resource]
        # Find the VPNEndpoint/Peer-VPNEndpoint field names
        vpnendpoint_field, peer_vpnendpoint_field = get_vpnendpoints_field(
                relation)

        # Get the list of IPsecEnforcers
        ipsecenforcers = (
            IPsecEnforcerInfo().get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(
                attrs[vpnendpoint_field])
        )

        peer_ipsecenforcers = (
            IPsecEnforcerInfo().get_vpnendpoint_to_ipsecenforcer_and_fqdn_list(
                attrs[peer_vpnendpoint_field])
        )

        if ipsecenforcers or peer_ipsecenforcers:
            raise serializers.ValidationError("Resource can not be deleted. "
                                              "The resource configuration is "
                                              "in use by IPsecEnforcer(s)")

    #
    # Reference check for Non-VPNBind records
    #
    dependencies = RESOURCE_DEPENDENCY_MAP.get(resource, None)

    if dependencies is None:
        return

    resources = dependencies[0]
    relations = [RESOURCE_TO_RELATION_MAP[relation] for relation in resources]

    fields = RESOURCE_DEPENDENCY_MAP[resource][1:]

    reference_exists = False
    for relation, field in itertools.product(relations, fields):
        value = attrs.get('id', None)
        if value is not None:
            records = storage.plugin.get_records(relation)
            for record in records:
                if record[field] == str(attrs['id']):
                    reference_exists = True
                    break

        if reference_exists:
            raise serializers.ValidationError("Resource can not be deleted. "
                                              "{0} with id {1} is in "
                                              "use".format(resource, str(value))
                                              )


def check_vpncertificate_exists(vpnbind_resource, vpnbind):
    """Check if the VPNEndpoint and Peer-VPNEndpoint has an associated
     VPNCertificate

    Args:
        vpnbind_resource (str): VPNBind Resource Name
        vpnbind (dict): VPNBind record

    Raises:
        serializers.ValidationError: If the VPNEndpoint or
            Peer-VPNEndpoint doesn't has an associated VPNCertificate

    """
    relation = RESOURCE_TO_RELATION_MAP[vpnbind_resource]
    # Find the VPNEndpoint/Peer-VPNEndpoint resource names
    vpnendpoint_resource, peer_vpnendpoint_resource = get_vpnendpoints_resource(
            relation)
    # Find the VPNEndpoint/Peer-VPNEndpoint field names
    endpoint_field, peer_endpoint_field = get_vpnendpoints_field(relation)

    # Check whether VPNEndpoint has an associated VPNCertificate
    vpnendpoint_relation = RESOURCE_TO_RELATION_MAP[vpnendpoint_resource]
    vpnendpoint_record = storage.plugin.get_record(vpnendpoint_relation,
                                                   vpnbind[endpoint_field])
    vpncertificate_id = vpnendpoint_record.get('vpncertificate_id', None)
    if vpncertificate_id is None:
        serializers.ValidationError(
                "VPNEndpoint with id {0} does not have an associated "
                "vpncertificate".format(vpnendpoint_record['id']))

    # Check whether Peer-VPNEndpoint has an associated VPNCertificate
    peer_vpnendpoint_relation = RESOURCE_TO_RELATION_MAP[
        peer_vpnendpoint_resource]
    peer_vpnendpoint_record = storage.plugin.get_record(
            peer_vpnendpoint_relation,
            vpnbind[peer_endpoint_field])
    vpncertificate_id = peer_vpnendpoint_record.get('vpncertificate_id', None)
    if vpncertificate_id is None:
        serializers.ValidationError(
                "VPNEndpoint with id {0} does not have an associated "
                "vpncertificate".format(peer_vpnendpoint_record['id']))

#
# VPN BIND Field checks
#


def check_id(field_name, resource_name, value):
    """Check whether record with 'id' exits in relation

    Args:
        field_name (str): field name in relation
        resource_name (str): resource name
        value (str): id of record

    Raises:
        serializers.ValidationError: When 'id' is invalid
    """
    if not storage.plugin.check_key(RESOURCE_TO_RELATION_MAP[resource_name],
                                    str(value)):
        raise serializers.ValidationError(
                "{0} {1} does not exist".format(field_name, str(value)))


def check_ikepolicy_id(value):
    """Check whether IKEPolicy exists

    Args:
        value (str): id of IKEPolicy
    """
    check_id('ikepolicy_id',
             'IKEPolicy',
             value)


def check_ipsecpolicy_id(value):
    """Check whether IPsecPolicy exists

    Args:
        value (str): id of IPsecPolicy
    """
    check_id('ipsecpolicy_id',
             'IPsecPolicy',
             value)


def check_vpnendpointgroup_id(value):
    """Check whether VPNEndpointGroup exists

    Args:
        value (str): id of VPNEndpointGroup
    """
    check_id('vpnendpointgroup_id',
             'VPNEndpointGroup',
             value)


def check_peer_vpnendpointgroup_id(value):
    """Check whether Peer VPNEndpointGroup exists

    Args:
        value (str): id of VPNEndpointGroup
    """
    check_id('peer_vpnendpointgroup_id',
             'VPNEndpointGroup',
             value)


def check_vpnendpointlocalsite_id(value):
    """Check whether VPNEndpointLocalSite exists

    Args:
        value (str): id of VPNEndpointLocalSite
    """
    check_id('vpnendpointlocalsite_id',
             'VPNEndpointLocalSite',
             value)


def check_peer_vpnendpointlocalsite_id(value):
    """Check whether Peer VPNEndpointLocalSite exists

    Args:
        value (str): id of VPNEndpointLocalSite
    """
    check_id('peer_vpnendpointlocalsite_id',
             'VPNEndpointLocalSite',
             value)


def check_peer_vpnendpointremotesite_id(value):
    """Check whether Peer VPNEndpointRemoteSite exists

    Args:
        value (str): id of VPNEndpointRemoteSite
    """
    check_id('peer_vpnendpointremotesite_id',
             'VPNEndpointRemoteSite',
             value)


def check_vpncertificate_id(value):
    """Check whether VPNCertificate exists

    Args:
        value (str): id of VPNCertificate
    """
    check_id('vpncertificate_id',
             'VPNCertificate',
             value)


def check_vpncacertificate_id(value):
    """Check whether VPNCACertificate exists

    Args:
        value (str): id of  VPNCACertificate
    """
    check_id('vpncacertificate_id',
             'VPNCACertificate',
             value)
