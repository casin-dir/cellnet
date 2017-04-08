#!/usr/bin/env bash

echo ""
echo "> freezing requirements ..."
pip freeze > requirements.txt
echo "> adding files ..."
git add .
git commit -m '$1'
echo "> pulling updates ..."
git pull origin $2
echo "> pushing updates ..."
git push origin $2
echo "> deactivating virtual env ..."
deactivate
echo "> READY"
echo ""