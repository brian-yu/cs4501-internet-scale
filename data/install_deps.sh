#!/usr/bin/env bash
apt-get update &&
# apt-get install python3-dev default-libmysqlclient-dev -y &&
apt-get install python3-dev -y &&
apt-get install python-pip -y &&
pip install kafka
# apt-get install python-mysqldb