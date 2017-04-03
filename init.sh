#!/usr/bin/env bash

echo ""
echo "> installing virtualenv ..."
pip install --upgrade virtualenv >> /dev/null
echo "> deleting old env..."
rm -rf env >> /dev/null
echo "> creating new env..."
virtualenv --no-site-packages -p python3 env >> /dev/null
echo "> READY"
echo ""


