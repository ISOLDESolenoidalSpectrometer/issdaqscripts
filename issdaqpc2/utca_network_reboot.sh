#!/bin/bash

utca_clear_serial.sh
echo "Shutdown the uTCA network card and reboot"
echo -ne '\r\nreboot\r\n' > /dev/ttyACM0
sleep 30
utca_fan_ctl.sh 8
