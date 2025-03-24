#!/bin/bash
sudo echo "Please wait around 1 minute for this to reboot!"
utca_clear_serial.sh
utca_fmc_off.sh
sleep 5.0
sudo service dhcpd restart
sleep 2.0
sudo service rpcbind restart
sleep 5.0
utca_clear_serial.sh
utca_network_reboot.sh
