#!/bin/bash

utca_clear_serial.sh
echo -ne 'shutdown 9\r\n' > /dev/ttyACM0
