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

"""ConfigAgent URL Configuration

The `urlpatterns` list routes URLs to views.

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from ConfigDB.views import MgmtUIView

from ConfigDB.api import views_api
urlpatterns = [
    url(r'^maas/', MgmtUIView.as_view(), name='ManagementUIView'),
    url(r'^(?P<version>(v1.0))/(?P<namespace>(secmon))/', include([
        url(r'^sflowassociation/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='sflowassociation_detail'),
        url(r'^sflowassociation/$',
            views_api.resource,
            name='sflowassociation_list'),
        url(r'^sflowassociation/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='sflowassociation_detail'),

        url(r'^netflowassociation/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='netflowassociation_detail'),
        url(r'^netflowassociation/$',
            views_api.resource,
            name='netflowassociation_list'),
        url(r'^netflowassociation/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='netflowassociation_detail'),

        url(r'^rawforwardassociation/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='rawforwardassociation_detail'),
        url(r'^rawforwardassociation/$',
            views_api.resource,
            name='rawforwardassociation_list'),
        url(r'^rawforwardassociation/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='rawforwardassociation_detail'),

        url(r'^netflowconfig/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='netflowconfig_detail'),
        url(r'^netflowconfig/$',
            views_api.resource,
            name='netflowconfig_list'),
        url(r'^netflowconfig/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='netflowconfig_detail'),

        url(r'^netflowmonitor/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='netflowmonitor_detail'),
        url(r'^netflowmonitor/$',
            views_api.resource,
            name='netflowmonitor_list'),
        url(r'^netflowmonitor/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='netflowmonitor_detail'),

        url(r'^collector/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='collector_detail'),
        url(r'^collector/$',
            views_api.resource,
            name='collector_list'),

        url(r'^collectorset/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='collectorset_detail'),
        url(r'^collectorset/$',
            views_api.resource,
            name='collectorset_list'),

        url(r'^policy/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='policy_detail'),
        url(r'^policy/$',
            views_api.resource,
            name='policy_list'),

        url(r'^sflowconfig/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='sflowconfig_detail'),
        url(r'^sflowconfig/$',
            views_api.resource,
            name='sflowconfig_list'),
        url(r'^sflowconfig/scope_id/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='sflowconfig_detail'),

        url(r'^scope/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='scope_detail'),
        url(r'^scope/$',
            views_api.resource,
            name='scope_list'),
        url(r'^scope/name/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='scope_detail'),

        url(r'^secmondetails/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='secmondetails_detail'),
        url(r'^secmondetails/$',
            views_api.resource,
            name='secmondetails_list'),
        # added for notification
        url(r'^secmondetails/scope_name/(?P<sk>[^/]+)/$',
            views_api.resource,
            name='secmondetails_detail'),

        url(r'^classificationobject/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='classificationobject_detail'),
        url(r'^classificationobject/$',
            views_api.resource,
            name='classificationobject_list'),

        url(r'^ruleobject/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='ruleobject_detail'),
        url(r'^ruleobject/$',
            views_api.resource,
            name='ruleobject_list'),

        url(r'^notification/(?P<pk>[^/]+)/$',
            views_api.resource,
            name='notification_detail'),
        url(r'^notification/$',
            views_api.resource,
            name='notification_list'),

    ])),
]
