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

from django.utils.translation import ugettext as _


INVALID_ENCRYPTION_ERR_MSG = _("encryption_algorithm has invalid choice(s) for "
                               "the record IKE version")

INVALID_INTEGRITY_ERR_MSG = _("integrity_algorithm has invalid choice(s) for "
                              "the IKE version")

INVALID_REAUTH_ERR_MSG = _("reauth value 'no' is not valid for IKE version 1")

IKE_MULTIPLE_DH_GROUP_ERR_MSG = _("Multiple dh_group values are not applicable "
                                  "for IKE version 1")

IKE_MULTIPLE_ENCRYPTION_ERR_MSG = _("Multiple encryption_algorithm values are "
                                    "not applicable for IKE version 1")

IKE_MULTIPLE_INTEGRITY_ERR_MSG = _("Multiple integrity_algorithm values are "
                                   "not for applicable IKE version 1")