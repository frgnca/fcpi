#!/bin/bash
################################################################################
# EXECUTEME.sh                                                                 #
#                                                                              #
# Requirements:                                                                #
#     A USB Flash Drive formatted in FAT32                                     #
#     A Raspberry Pi with a Camera Module                                      #
#     A fresh installation of Raspbian Jessie                                  #
#     The following files in /home/pi/fcpi/                                    #
#         LICENCE                                                              #
#         README.md                                                            #
#         EXECUTEME.sh                                                         #
#         fcpi-update.sh                                                       #
#         fcpi.py                                                              #
#         fcpi.service                                                         #
#         fcpi.sh                                                              #
#                                                                              #
# Instructions:                                                                #
#     chmod +x EXECUTEME.sh                                                    #
#     sudo ./EXECUTEME.sh                                                      #
################################################################################

# Setup folder to mount USB Flash Drive
mkdir /media/usb/
chmod  700 /media/usb/

chmod 700 /home/pi/fcpi/fcpi-update.sh

# Setup systemd service for fcpi.sh
cp fcpi.service /etc/systemd/system/fcpi.service
chmod 700 /etc/systemd/system/fcpi.service
chmod 700 /home/pi/fcpi/fcpi.sh
# Reload and start new service
systemctl daemon-reload
systemctl enable fcpi.service
systemctl start fcpi.service

## Set static IP address for wifi in /etc/dhcpcd.conf
#echo "
## Static IP
#interface wlan0
#static ip_address=192.168.1.41/24
#static routers=192.168.1.1
#static domain_name_servers=8.8.8.8, 8.8.4.4" >> /etc/dhcpcd.conf
## Reload dhcpcd
#dhcpcd -n

# Set camera in /boot/config.txt
echo "
# Camera
start_x=1
gpu_mem=128
#disable_camera_led=1" >> /boot/config.txt
# Reboot necessary to take effect
reboot
