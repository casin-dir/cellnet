#!/usr/bin/env bash
source env/bin/activate
echo "> virtual env activated"
pip install -r requirements.txt >> /dev/null
echo "> requirements downloaded"
echo "> READY"