#!/bin/bash

python3 automate.py -c domain -d 60 -t send:siem
python3 automate.py -c ip -d 60 -t send:siem
python3 automate.py -c email -d 60 -t send:siem
