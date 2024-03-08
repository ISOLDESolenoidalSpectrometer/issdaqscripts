#!/bin/bash

utca_clear_serial.sh
echo -ne 'fru_start 30\r\n' > /dev/ttyACM0
