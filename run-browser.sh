#!/usr/bin/bash
cd /root/robz/rz-browser/
uv run uvicorn main:app  --host=0.0.0.0 --workers=4 --port=5000
