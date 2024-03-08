#!/bin/bash

utca_clear_serial.sh
echo "Powering down"
utca_fmc_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up"
utca_fmc_on.sh
