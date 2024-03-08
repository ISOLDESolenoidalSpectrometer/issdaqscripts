#!/bin/bash

for i in 0 1 2 3
do
	screen_name=iss0$i

	screen -ls $screen_name | grep -E '\s+[0-9]+\.' | awk -F ' ' '{print$1}' | while  read s;
	do screen -XS $s quit;
	done

	screen_name=rates_iss0$i

	screen -ls $screen_name | grep -E '\s+[0-9]+\.' | awk -F ' ' '{print$1}' | while  read s;
	do screen -XS $s quit;
	done
done

iss00_id=`python3 ~/scripts/get_serial_address.py iss00`
iss01_id=`python3 ~/scripts/get_serial_address.py iss01`
iss02_id=`python3 ~/scripts/get_serial_address.py iss02`
iss03_id=`python3 ~/scripts/get_serial_address.py iss03`

screen -dmS iss00 $iss00_id
screen -dmS iss01 $iss01_id
screen -dmS iss02 $iss02_id
screen -dmS iss03 $iss03_id

screen -dmS rates_iss00 `rates_iss_channels.py 0`
screen -dmS rates_iss01 `rates_iss_channels.py 1`
screen -dmS rates_iss02 `rates_iss_channels.py 2`
#screen -dmS rates_iss03 `rates_iss_channels.py 3`
