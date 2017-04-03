#!/usr/bin/env bash

pip freeze > requirements.txt
git add .
git commit -m '$1'
git pull origin $2
git push origin $2