#!/bin/bash

echo "Powering down iss02"
utca_iss02_off.sh
sleep 5
echo "Powering up iss02"
utca_iss02_on.sh
