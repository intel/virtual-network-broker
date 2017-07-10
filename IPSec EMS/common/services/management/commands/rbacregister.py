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

from __future__ import unicode_literals
import logging

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
import requests

from services.api.rbac_settings import RBAC_PROJECT, RBAC_URI

LOG = logging.getLogger(__name__)

PROJECT = 'ipsecems'
RBAC_PROJECT_REGISTER_ENDPOINT = '/v1/main/auth/register_project/'


class Command(BaseCommand):
    help = "Register project with local RBAC Service"

    def handle(self, *args, **options):
        try:
            url = RBAC_URI + RBAC_PROJECT_REGISTER_ENDPOINT
            response = requests.request(method='POST',
                                        url=url,
                                        data={'name': PROJECT})
            print _("%s project got registered") % PROJECT
        except requests.exceptions.RequestException as e:
            print _("Error registering the project %s. Check logs for details")\
                  % RBAC_PROJECT
            LOG.error('%s %s' % (e.__doc__, e.message))
