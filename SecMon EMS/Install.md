# **SecMon EMS Setup Steps**
========================

## Install Dependencies
--------------------

1.  Install packages used by SecMon EMS server. Like *Django Framework, python-consul and Django Rest Framework.*
    `apt-get -y update`
    `apt-get -y --force-yes install python-pip`
    `pip install Django==1.8.1`
    `apt-get -y --force-yes install python-yapsy`
    `pip install python-consul`
    `pip install djangorestframework==2.3.12`

2.  Fetch **consul** distributed database binary from hashicorp website.
    `cd <repo_name>/SecMonEMS/`
    `wget --no-check-certificate https://releases.hashicorp.com/consul/0.7.0/consul_0.7.0_linux_amd64.zip`
    `unzip consul_0.7.0_linux_amd64.zip`
    `rm consul_0.7.0_linux_amd64.zip`

3.  Create folder to store **consul** database files.
    `cd <repo_name>/SecMonEMS/`
    `mkdir -p consul_data`

## Run SecMon EMS Server
---------------------

1.  Start **consul** database server in bootstrap mode in background.
    `cd <repo_name>/SecMonEMS/`
    `nohup ./consul agent -server -bootstrap -data-dir consul_data
    -advertise=127.0.0.1 &`

2.  Start **Django server** on **localhost** port **9082.** And start
    **EMS Notifier** service in background.
    `cd <repo_name>/SecMonEMS/SecMonEMS`
    `nohup python ./manage.py runserver 0.0.0.0:9082 &`
    `nohup python ./manage.py emsnotify &`


