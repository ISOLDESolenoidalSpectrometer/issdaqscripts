#!/bin/bash

utca_clear_serial.sh
echo -ne 'shutdown 6\r\n' > /dev/ttyACM0
