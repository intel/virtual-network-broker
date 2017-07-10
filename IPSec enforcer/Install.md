# **IPsec Enforcer Setup Steps**
============================

## Install Dependencies
--------------------

1.  Install packages used by IPsec Enforcer. Like **Django Framework,
    python-consul, Django Rest Framework and etc**.
    `cd <repo_name>/enforcer/`
    `apt-get -y update`
    `apt-get -y --force-yes install python-pip`
    `apt-get -y --force-yes install python-dev`
    `apt-get -y --force-yes install libldap2-dev`
    `apt-get -y --force-yes install libsasl2-dev`
    `apt-get -y --force-yes install libssl-dev`
    `apt-get -y --force-yes install strongswan`
    `pip install -r requirements_ipsecenforcer.txt`

## Configure IPsec Enforcer
------------------------

1.  Open IPsec enforcer configuration file.
    `cd <repo_name>/enforcer/ipsec_enforcer/registration/`
    `vim ipsecenforcer.ini`

2.  Change **Endpoint** section. Mention type of endpoint **(group
    or localsite)** and name of endpoint. **First** **field** contains
    **name** of endpoint and **second** **field** contains **type**
    of endpoint. For ex:
    `NAME_AND_TYPE = (group1, group)`

3.  Change **Interface** section. Mention interface should be used for
    **tunnel creation** and interface should be used to communicate to
    IPsec EMS server. For ex:
    `IPSEC_TUNNEL_INTERFACE = eth1`
    `IPSEC_EMS_INTERFACE = eth0`

4.  Change **IPsec EMS controller** section. Mention **IP address and
    port** of IPsec EMS server. For ex:
    `IP_ADDRESS_WITH_PORT = 192.168.1.105:8000`

5.  Change **IPsec EMS** section with same data as **step 4**.

## Run IPsec Enforcer
------------------

1.  Start **IPsec enforcer** server.
    `cd <repo_name>/enforcer/ipsec_enforcer/`
    `nohup python manage.py runserver 0.0.0.0:8001 &`

2.  Start **IPsec enforcer** agent.
    `cd <repo_name>/enforcer/ipsec_enforcer/`
    `nohup python manage.py ipsecenforcer_agent &`

3.  Now start **strongswan** to create IPsec Tunnel between enforcers.
    Enforcer populate ipsec.conf and ipsec.secrets files on the basis of
    configurations mentioned in IPsec EMS.
    `ipsec start`

4.  If IPsec configurations are changed, then **restart** **strongswan**
    service so that strongswan can see updated configuraions.


