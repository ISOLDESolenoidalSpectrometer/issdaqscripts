#!/bin/bash

utca_clear_serial.sh
echo "Powering down iss00"
utca_iss00_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up iss00"
utca_iss00_on.sh
