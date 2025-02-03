#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

waybar -c $SCRIPT_DIR/waybar.jsonc > /dev/null 2>&1 &
WAYBAR_PID=$!
firefox https://gabbia.org/
# SIGTERM does not work? Why?
kill -9 $WAYBAR_PID

