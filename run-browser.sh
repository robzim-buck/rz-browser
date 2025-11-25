#!/bin/bash
set -e
cd /root/robz/rz-browser/ || exit 1
exec /root/robz/rz-browser/.venv/bin/python /root/robz/rz-browser/main.py
