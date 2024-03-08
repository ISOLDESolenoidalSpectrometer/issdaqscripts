#!/bin/bash

utca_clear_serial.sh
echo -ne 'shutdown 14\r\n' > /dev/ttyACM0
