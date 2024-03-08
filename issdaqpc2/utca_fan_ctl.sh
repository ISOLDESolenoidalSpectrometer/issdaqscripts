#/bin/bash

# Get the fan speed as the first argument
FAN_SPEED=$1

# Check that an argument is given
if [[ -z "$1" ]]
then
	echo "ERROR: No argument given. Please supply a fan speed between 5 and 10 (inclusive). Exiting..."
	exit
fi

# Check that argument is an integer
re='^[0-9]+$'
if ! [[ $1 =~ $re ]]
then
	echo "ERROR: Argument \"${1}\" invalid - I need an integer! Exiting..."
	exit
fi


# Check that no other arguments are given
if [[ $# -ne 1 ]]
then
	echo "WARNING: additional arguments supplied. Will ignore these..."
fi

# Check that the speed is within the normal bounds ( 5 <= speed <= 10 )
if [[ $FAN_SPEED -le 4 ]]
then
	echo "ERROR: fan speed is normally 5 (maximum 10). Please do not set below this level. Exiting..."
	exit
elif [[ $FAN_SPEED -ge 11 ]]
then
	echo "ERROR: fan speed has a maximum of 10. Do not exceed this! Exiting..."
	exit
fi

# Set the fan speed
# 3 = set fan speed, 1 or 2 = which side
utca_clear_serial.sh
echo -e "fan_ctl\r\n3\r\n1\r\n${FAN_SPEED}\r\n" > /dev/ttyACM0
echo -e "fan_ctl\r\n3\r\n2\r\n${FAN_SPEED}\r\n" > /dev/ttyACM0
echo "Set fan speed to ${FAN_SPEED}. Listen/feel to see if it worked on both sides!"
