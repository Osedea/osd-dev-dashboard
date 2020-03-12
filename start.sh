#!/bin/bash

parallel ::: \
    "conky -d -p 5 -c ~/.conky/config/conky_attendance" \
    "conky -d -p 5 -c ~/.conky/config/conky_toggl" \
    "conky -d -p 5 -c ~/.conky/config/conky_weather" \
    "conky -d -p 5 -c ~/.conky/config/conky_github" \
    "conky -d -p 5 -c ~/.conky/config/conky_gcalendar" \
    "conky -d -p 5 -c ~/.conky/config/conky_gmail"
