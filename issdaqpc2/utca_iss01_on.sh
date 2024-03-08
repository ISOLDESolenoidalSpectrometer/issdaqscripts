#!/bin/bash

utca_clear_serial.sh
echo -ne 'fru_start 10\r\n' > /dev/ttyACM0
