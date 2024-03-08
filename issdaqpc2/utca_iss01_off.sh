#!/bin/bash

utca_clear_serial.sh
echo -ne 'shutdown 10\r\n' > /dev/ttyACM0
