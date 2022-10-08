#!/bin/bash
mkdir /opt/minecraft-standby
cp data/* /opt/minecraft-standby/
cp minecraft-standby.service /usr/lib/systemd/system/
yum install python3-devel gcc systemd-devel -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
systemctl daemon-reload
systemctl enable minecraft-standby.service --now