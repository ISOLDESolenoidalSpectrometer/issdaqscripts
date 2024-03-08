#!/bin/bash

utca_clear_serial.sh
echo "Powering down iss02"
utca_iss02_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up iss02"
utca_iss02_on.sh
