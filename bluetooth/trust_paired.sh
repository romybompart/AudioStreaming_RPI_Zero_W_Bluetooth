#!/bin/bash
#bring down wireless lan driver as it interferes with bluetooth audio...
sudo ifdown wlan0
# Power on the bluetooth controller and make it discoverable and pairable
echo -e 'power on \nagent on\ndefault-agent\ndiscoverable on \npairable on\nquit' | bluetoothctl
while true
do
        # List devices
        echo -e 'paired-devices\nquit' | bluetoothctl | awk '/^Device/ {print $2 "\t" $3}' > devices.tmp
        # Trust devices
        while read p
        do
                echo "Device to trust is: $p"
                mymac=$( echo $p | cut -d' ' -f 1 )
                echo -e "trust $mymac \nquit" | bluetoothctl
        done < devices.tmp
        # Remove temporary file
        rm devices.tmp
        sleep 15
done
