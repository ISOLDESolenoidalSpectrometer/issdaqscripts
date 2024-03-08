#!/bin/bash

utca_clear_serial.sh
echo "Powering down R3BCST"
utca_cst_off.sh
sleep 5
utca_clear_serial.sh
echo "Powering up R3BCST"
utca_cst_on.sh
