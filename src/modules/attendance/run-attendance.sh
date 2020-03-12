#!/bin/bash
if [[ -z "$(ps aux | awk '{print $2}' | grep $(cat src/modules/attendance/pid.file))" ]]
then 
    python3 src/modules/attendance/attendance.py&
    echo "$\!" > src/modules/attendance/pid.file 
fi
