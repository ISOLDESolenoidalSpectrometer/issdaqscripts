#!/bin/bash

echo "Powering down iss03"
utca_iss03_off.sh
sleep 5
echo "Powering up iss03"
utca_iss03_on.sh
