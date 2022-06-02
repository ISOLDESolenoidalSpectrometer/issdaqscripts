#!/bin/bash

echo "Shutdown the uTCA system and reboot"
echo -ne 'shutdown system\r\n' > /dev/ttyACM0
