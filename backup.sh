#!/usr/bin/env bash

# check if server is running and start it if it's not
/Applications/CopyQ.app/Contents/MacOS/CopyQ tabs
RESULT=$?
if [ $RESULT -ne 0 ]; then
  /Applications/CopyQ.app/Contents/MacOS/CopyQ &
  sleep 1
fi


script_dir=`dirname "${BASH_SOURCE[0]}"`
cd $script_dir
./venv/bin/python -c "from refresh_backup import run_backup as r;r()" 1>>./stdout.log 2>>./stderr.log