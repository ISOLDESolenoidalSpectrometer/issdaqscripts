#!/bin/bash

utca_clear_serial.sh
echo -ne 'shutdown 30\r\n' > /dev/ttyACM0
