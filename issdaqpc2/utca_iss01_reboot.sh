#!/bin/bash

utca_clear_serial.sh
echo "Powering down iss01"
utca_iss01_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up iss01"
utca_iss01_on.sh
