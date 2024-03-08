#!/bin/bash

DATADIR="/TapeData/IS686"
CONFIGDIR="/home/isslocal/calibrations"
SETTINGSFILE="settings_110Sn_20220927.dat"
CALIBFILE="calibration_is686_20220928.cal"
REACTIONFILE="reaction_110Sn_20220927.dat"

CURTIME=$(date +%Y%m%d_%H%M%S)

shopt -s extglob

# Position 3 runs
#DATAFILES+=" $DATADIR/R@(54|56|58|59|60|92|93|94)_+([0-9])"

# Position 4 runs
DATAFILES+=" $DATADIR/R@(43|44|45|46|47|48|49|50|51|52)_+([0-9])"

# Position 5 runs
DATAFILES+=" $DATADIR/R@(68|69|70|71|72|73|74|75|76|77|78)_+([0-9])"

# Position 6 runs
DATAFILES+=" $DATADIR/R@(27|30|31|32|33|35|41|42)_+([0-9])"

# Position 7 runs
DATAFILES+=" $DATADIR/R@(79|80|87|88|89|90)_+([0-9])"

# Position 8 runs
DATAFILES+=" $DATADIR/R@(3|4|5|6|7|8|9|11|12|13|15|16|20|21|22|23|24|25|26)_+([0-9])"



## Histogram them all together
iss_sort -s $CONFIGDIR/$SETTINGSFILE -c $CONFIGDIR/$CALIBFILE -r $CONFIGDIR/$REACTIONFILE -i $DATAFILES -o 110Sn_sum_hists_${CURTIME}.root
