#!/bin/bash

echo "Powering down R3BCST"
utca_cst_off.sh
sleep 5
echo "Powering up R3BCST"
utca_cst_on.sh
