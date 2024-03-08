#!/bin/bash

utca_clear_serial.sh
echo "Shutdown the uTCA system and reboot"
echo -ne '\r\nshutdown system\r\n' > /dev/ttyACM0
sleep 5
utca_fan_ctl.sh 8
