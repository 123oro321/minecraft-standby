#!/bin/bash
mkdir /opt/minecraft-standby
cp data/* /opt/minecraft-standby/
cp minecraft-standby.service /usr/lib/systemd/system/
pip3 install -r requirement.py
systemctl daemon-reload
systemctl enable minecraft-standby.service --now