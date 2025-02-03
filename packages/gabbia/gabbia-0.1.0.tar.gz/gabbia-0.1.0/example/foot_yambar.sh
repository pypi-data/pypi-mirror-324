#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

yambar -c $SCRIPT_DIR/yambar.yml > /dev/null 2>&1 &
YAMBAR_PID=$!
foot
kill $YAMBAR_PID
