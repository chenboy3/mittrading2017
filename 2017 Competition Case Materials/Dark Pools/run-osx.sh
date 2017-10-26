#!/bin/bash

./utils/mangocore-osx-amd64.x --case ./samples/main$1.json --identity ./utils/identity.json --start 5
sleep 5
python utils/bot.py
