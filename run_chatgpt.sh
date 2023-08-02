#!/bin/bash

if [[ -z "$1" ]]; then
    python3.10 main.py
else
    python3.10 main.py "$@"
fi
