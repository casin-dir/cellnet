#!/usr/bin/env bash

echo ""
echo "> pulling ..."
git pull >> /dev/null
echo "> activating virtual env ..."
. env/bin/activate >> /dev/null
echo "> installing requirements ..."
pip install -r requirements.txt >> /dev/null
echo "> READY"
echo ""