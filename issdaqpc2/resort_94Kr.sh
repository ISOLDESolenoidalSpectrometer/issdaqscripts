#!/bin/bash

DATADIR="/TapeData/IS711"
CONFIGDIR="/home/isslocal/calibrations"
SETTINGSFILE="settings_Kr_20221024.dat"
CALIBFILE="calibration_is711_20221024.cal"
REACTIONFILE="reaction_94Kr_20221024.dat"

CURTIME=$(date +%Y%m%d_%H%M%S)

shopt -s extglob

# Position 3 runs
DATAFILES+=" $DATADIR/R@(90|92|93|94|95|98|99|100|101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|118|119|120|121|122|123|124|125|126|127)_+([0-12])"



## Histogram them all together
iss_sort -s $CONFIGDIR/$SETTINGSFILE -c $CONFIGDIR/$CALIBFILE -r $CONFIGDIR/$REACTIONFILE -i $DATAFILES -o 94Kr_sum_hists_${CURTIME}.root
