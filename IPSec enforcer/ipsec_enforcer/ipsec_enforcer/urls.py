"""ipsec_enforcer URL Configuration

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

from registration.api.views_heartbeat import ipsecenforcer_heartbeat
from registration.api.views_config_update import ipsecenforcer_config_update

urlpatterns = [
    url(r'^admin/', admin.site.urls),

     url(r'^(?P<version>(v1))/(?P<namespace>(main))/ipsecvpn/',
        include([
            url(r'^heartbeat/(?P<pk>[^/]+)/$',
                ipsecenforcer_heartbeat,
                name='heartbeat_detail'),
            url(r'^configupdate/(?P<pk>[^/]+)/$',
                ipsecenforcer_config_update,
                name='config_update_detail'),
        ])),
]
