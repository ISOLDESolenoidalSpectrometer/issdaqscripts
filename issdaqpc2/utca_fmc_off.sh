#!/bin/bash

utca_clear_serial.sh
echo -ne '\r\nshutdown all\r\n' > /dev/ttyACM0
