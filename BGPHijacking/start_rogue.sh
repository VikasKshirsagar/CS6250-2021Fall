#!/bin/bash

# Copyright 2021
# Georgia Tech
# All rights reserved
# Do not post or publish in any public or forbidden forums or websites

echo "Killing any existing rogue AS"
./stop_rogue.sh

echo "Starting rogue AS"
sudo python run.py --node R6 --cmd "/usr/lib/frr/zebra -f conf/zebra-R6.conf -d -i /tmp/zebra-R6.pid > logs/R6-zebra-stdout"
sudo python run.py --node R6 --cmd "/usr/lib/frr/bgpd -f conf/bgpd-R6.conf -d -i /tmp/bgpd-R6.pid > logs/R6-bgpd-stdout"
