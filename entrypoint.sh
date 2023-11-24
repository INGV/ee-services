#!/bin/sh

# Below shells script is required because the flask container need to wait for postgres db server to startup before
# accessing it below.

#if [ ! -d /opt/log ]; then
#   mkdir -p /opt/log
#   chmod -R 777 /opt/log
#fi

# Run below commands from manage.py to initialize db and have some default data.
uwsgi --ini /etc/uwsgi.ini