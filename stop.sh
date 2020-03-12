#!/bin/bash

ps aux | grep conky | awk '{print $2}' | xargs -n 1 -I {} kill {} &> /dev/null 

# kill -TERM "$(cat ~/.conky/process.pid)" && rm ~/.conky/process.pid