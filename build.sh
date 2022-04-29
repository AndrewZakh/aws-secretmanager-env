#!/bin/bash
pip3 install -U nuitka
nuitka3 --standalone --onefile secrets.py
