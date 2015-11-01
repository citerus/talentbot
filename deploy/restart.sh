#!/bin/bash

pkill -f 'python2.7 main.py'
cd ~/talentbot

source keys.sh
nohup python2.7 main.py &

