#!/bin/bash

utca_clear_serial.sh
echo -ne '\r\nfru_start 30\r\nfru_start 9\r\nfru_start 6\r\nfru_start 10\r\n' > /dev/ttyACM0
