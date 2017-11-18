#### What is fcpi?
An installation script to configure a Raspberry Pi with a Camera Module using the PiCamera package in python. The final product can be plugged and forgotten. It records one minute videos to a connected usb flash drive and delete the oldest videos when storage space become insufficient.

#### Requirements:
- A USB Flash Drive formatted in FAT32
- A Raspberry Pi with a Camera Module
- A fresh installation of Raspbian Jessie

#### Instructions:

    git clone https://github.com/frgnca/fcpi.git
    cd fcpi/
    chmod +x EXECUTEME.sh
    sudo ./EXECUTEME.sh
