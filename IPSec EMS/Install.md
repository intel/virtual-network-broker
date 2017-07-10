# **IPsec EMS Setup Steps**
==================================

## Install Dependencies
--------------------

1.  Install packages used by IPsec EMS server. Like **Django Framework,
    python-consul, Django Rest Framework and etc**.
```
    cd <repo_name>
    apt-get -y update
    apt-get -y --force-yes install python-pip
    apt-get -y --force-yes install python-dev
    apt-get -y --force-yes install libldap2-dev
    apt-get -y --force-yes install libsasl2-dev
    apt-get -y --force-yes install libssl-dev
    pip install -r common/requirements_ipsecems.txt
    pip install -r rbac/requirements_ipsecems_rbac.txt
```

2.  Fetch **consul** distributed database binary from hashicorp website.
```
    cd <repo_name>
    wget --no-check-certificate
    https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip
    unzip consul_0.6.4_linux_amd64.zip
    rm consul_0.6.4\_linux_amd64.zip
```

3.  Create folder to store **consul** database files.
```
    cd <repo_name>/
    mkdir -p consul_data
    mkdir -p consul.d
```

Run IPsec EMS Server
--------------------

1.  Start **consul** database server in bootstrap mode in background.
```    
    cd <repo_name>/
    nohup ./consul agent -server -bootstrap-expect 1 -data-dir
    consul_data -node=agent-one -config-dir consul.d -advertise=127.0.0.1 &
```

1.  Start **RBAC** server in background. Which will manage user and
    their respective roles.
```    
    cd <repo_name>/rbac/
    nohup python manage.py runserver localhost:8051 &
```

2.  Start **IPsec EMS** server in background. Which will communicate
    with **RBAC** server and server GUI pages to user.
```    
    cd <repo_name>/common/
    nohup python manage.py runserver 0.0.0.0:8000 &
    nohup python manage.py healthcheck &
    nohup python manage.py ipsecenforcernotify &
    nohup python manage.py rbacregister &
```

