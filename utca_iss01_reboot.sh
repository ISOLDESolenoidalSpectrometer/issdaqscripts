#!/bin/bash

echo "Powering down iss01"
utca_iss01_off.sh
sleep 5
echo "Powering up iss01"
utca_iss01_on.sh
