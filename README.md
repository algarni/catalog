# Catalog App
This work is part of Udacity Full Stack Nondegree program. The purpose of this work to explore some basic concepts regarding CRUD operation, authentication & authorization in python. 

# Download Source Code from GitHub
`https://github.com/algarni/catalog.git`

# Prerequisites

1. [Python 3.7](https://www.python.org/ftp/python/3.7.1/python-3.7.1.exe)
2. [VirtualBox 5.2](https://download.virtualbox.org/virtualbox/5.2.22/VirtualBox-5.2.22-126460-Win.exe)
3. [Vagrant 2.2.1 (Windows 64-bit)](https://releases.hashicorp.com/vagrant/2.2.1/vagrant_2.2.1_x86_64.msi)
4. [Download the VM configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
5. Install the following python packages:
~~~~
blinker==1.4
Flask==1.0.2
Flask-Bootstrap==3.3.7.1
Flask-Dance==1.2.0
Flask-Login==0.4.1
Flask-Migrate==2.3.1
Flask-SQLAlchemy==2.3.2
~~~~

6. Set the fllowing environment variable in your machine to disable HTTPS requirement:
~~~~
$ export OAUTHLIB_INSECURE_TRANSPORT=1
$ export OAUTHLIB_RELAX_TOKEN_SCOPE=1
~~~~

# Usage
~~~~
$ export OAUTHLIB_INSECURE_TRANSPORT=1
$ export OAUTHLIB_RELAX_TOKEN_SCOPE=1
$ cd catalog/
$ python3 applicaton.py
~~~~

# License
MIT

