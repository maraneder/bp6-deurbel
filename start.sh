#!/usr/bin/env bash

touch /tmp/start_triggered

sleep 10
echo "Start Deurbel"
/home/Mara/lamp-venv/bin/python /home/Mara/blue/hue/lamp_blink.py
/usr/bin/python2 /home/Mara/school/button.py
