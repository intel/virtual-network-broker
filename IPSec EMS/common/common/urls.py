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


"""common URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin

from services.api import (
    views_api_resource, views_authentication, views_certificate,
    views_enforcer_registration
)
from services.api.views_mgmt_ui import MgmtUIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ipsecems/', MgmtUIView.as_view(), name='ManagementUIView'),
    url(r'^(?P<version>(v1))/(?P<namespace>(main))/ipsecvpn/',
        include([

            url(r'^ikepolicies/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='ikepolicies_detail'),
            url(r'^ikepolicies/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='ikepolicies_list'),

            url(r'^ipsecpolicies/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='ipsecpolicies_detail'),
            url(r'^ipsecpolicies/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='ipsecpolicies_list'),

            url(r'^vpnbindgrouptogroup/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnbindgrouptogroup_detail'),
            url(r'^vpnbindgrouptogroup/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnbindgrouptogroup_list'),

            url(r'^vpnbindgrouptolocalsite/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnbindgrouptolocalsite_detail'),
            url(r'^vpnbindgrouptolocalsite/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnbindgrouptolocalsite_list'),

            url(r'^vpnbindgrouptoremotesite/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnbindgrouptoremotesite_detail'),
            url(r'^vpnbindgrouptoremotesite/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnbindgrouptoremotesite_list'),

            url(r'^vpnbindlocalsitetolocalsite/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnbindlocalsitetolocalsite_detail'),
            url(r'^vpnbindlocalsitetolocalsite/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnbindlocalsitetolocalsite_list'),

            url(r'^vpnbindlocalsitetoremotesite/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnbindlocalsitetoremotesite_detail'),
            url(r'^vpnbindlocalsitetoremotesite/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnbindlocalsitetoremotesite_list'),

            url(r'^vpnendpointgroups/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnendpointgroups_detail'),
            url(r'^vpnendpointgroups/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnendpointgroups_list'),

            url(r'^vpnendpointlocalsites/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnendpointlocalsites_detail'),
            url(r'^vpnendpointlocalsites/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnendpointlocalsites_list'),

            url(r'^vpnendpointremotesites/(?P<pk>[^/]+)/$',
                views_api_resource.GenericRetrieveUpdateDestroyResourceView.as_view(),
                name='vpnendpointremotesites_detail'),
            url(r'^vpnendpointremotesites/$',
                views_api_resource.GenericListCreateResourceView.as_view(),
                name='vpnendpointremotesites_list'),

            url(r'^ipsecenforcerregistrations/(?P<pk>[^/]+)/$',
                views_enforcer_registration.ipsec_enforcer_registration,
                name='ipsecenforcerregistrations_detail'),
            url(r'^ipsecenforcerregistrations/$',
                views_enforcer_registration.ipsec_enforcer_registration,
                name='ipsecenforcerregistrations_list'),

            url(r'^vpncacertificates/(?P<pk>[^/]+)/$',
                views_certificate.resource,
                name='vpncacertificates_detail'),
            url(r'^vpncacertificates/$',
                views_certificate.resource,
                name='vpncacertificates_list'),

            url(r'^vpncertificates/(?P<pk>[^/]+)/$',
                views_certificate.resource,
                name='vpncertificates_detail'),
            url(r'^vpncertificates/$',
                views_certificate.resource,
                name='vpncertificates_list'),

            url(r'^auth/', views_authentication.resource),
        ])),

    url(r'^(?P<version>(v1))/(?P<namespace>(main))/auth/', views_authentication.resource),
]
