#!/bin/bash
echo -e 'power off \nquit' | bluetoothctl
sleep 5
echo -e 'power on \nquit' | bluetoothctl
sleep 5
echo -e 'power off \nquit' | bluetoothctl
sleep 5
echo -e 'power on \nquit' | bluetoothctl


while true
do
        echo -e 'paired-devices\nquit' | bluetoothctl | awk '/^Device/ {print $2 "\t" $3}' > devices.tmp
        while read p
        do
                echo "Device to trust is: $p"
                mymac=$( echo  $p | cut -d' ' -f 1 )
                echo -e "trust $mymac \nquit" | bluetoothctl
        done < devices.tmp

        rm devices.tmp
        sleep 15
done
