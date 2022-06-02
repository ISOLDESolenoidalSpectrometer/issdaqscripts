#!/bin/bash

echo "Powering down iss00"
utca_iss00_off.sh
sleep 5
echo "Powering up iss00"
utca_iss00_on.sh
