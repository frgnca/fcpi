#!/bin/bash
################################################################################
# fcpi-update.sh                                                               #
################################################################################

## Get Linux up to date using apt-get
#apt-get update
#apt-get -y upgrade

# Update fcpi folder using git
cd /home/pi/fcpi/
git pull https://github.com/frgnca/fcpi.git

# Restart fcpi service using systemctl
systemctl stop fcpi.service
systemctl disable fcpi.service
systemctl daemon-reload
systemctl enable fcpi.service
systemctl start fcpi.service
