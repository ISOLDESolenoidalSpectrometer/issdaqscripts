#!/bin/bash

utca_clear_serial.sh
echo "Powering down iss03"
utca_iss03_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up iss03"
utca_iss03_on.sh
