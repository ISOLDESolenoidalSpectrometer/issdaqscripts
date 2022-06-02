#!/bin/bash

echo "Powering down"
utca_fmc_off.sh
sleep 5
echo "Powering up"
utca_fmc_on.sh
