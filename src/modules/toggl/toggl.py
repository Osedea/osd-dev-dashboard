
#! /usr/bin/env python3

import requests
import os
from sys import stderr
from datetime import datetime, timedelta, timezone
# import toggl_generator
from tabulate import tabulate


script_directory = os.path.dirname(os.path.realpath(__file__))

try:
    with open('{}/security/.toggl_token'.format(script_directory), 'r') as f:
        token = f.read().strip()

    assert len(token) > 0
except Exception as e:
    print('''Your toggl API token is missing from '~/.conky/src/modules/toggl/security/.toggl_token' it can be found on https://toggl.com/app/profile''', file=stderr)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def format_entry(entry):
    start = utc_to_local(datetime.fromisoformat(entry["start"]))
    if "stop" in entry:
        end = utc_to_local(datetime.fromisoformat(entry["stop"]))
    else:
        end = datetime.now()

    start_time = datetime.strptime('{start_day:02d}:{start_hour:02d}:{start_minute:02d}'.format(
        start_day=start.day, start_hour=start.hour, start_minute=start.minute), '%d:%H:%M')
    end_time = datetime.strptime('{end_day:02d}:{end_hour:02d}:{end_minute:02d}'.format(
        end_day=end.day, end_hour=end.hour, end_minute=end.minute), '%d:%H:%M')
    diff = end_time - start_time

    if "stop" in entry:
        hour = '{start_hour:02d}:{start_minute:02d} - {stop_hour:02d}:{stop_minute:02d}'
    else:
        hour = '{start_hour:02d}:{start_minute:02d} - '

    return (
        '>' if not "stop" in entry else '',
        '{hour:02d}h{minute:02d}'.format(
            hour = int(diff.seconds/3600), minute = int((diff.seconds % 3600)/60)),
        hour.format(
            start_hour = start.hour, start_minute=start.minute,
            stop_hour = end.hour, stop_minute=end.minute
        ),
        '{description}'.format(
            description = entry["description"]
        )
    )


def extract_time(json):
    if "stop" in json:
        return utc_to_local(datetime.fromisoformat(json["stop"]))
    else:
        return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None)


def authentication():
    # sending get request and saving the response as response object
    r = requests.get(url='https://www.toggl.com/api/v8/me',
                     auth=(token, 'api_token'))
    # extracting data in json format
    data = r.json()
    return data


def time_entries_now():
    start = (datetime.now().replace(hour = 0, minute = 0, second = 0,
                                    microsecond = 0).isoformat() + '-04:00').replace(':', '%3A')
    r = requests.get(url = 'https://www.toggl.com/api/v8/time_entries?start_date=' +
                     start, auth = (token, 'api_token'))
    # extracting data in json format
    data = r.json()
    data.sort(key = extract_time, reverse=True)
    return data


def get_time_entries_today():
    data = time_entries_now()
    entries = []
    for entry in data:
        entries.append(format_entry(entry))
    return data


if __name__ == '__main__':
    data = get_time_entries_today()
    if not data:
        print(
            tabulate(
                [[
                    'No Entries for Today - {}'.format(
                        datetime.now().strftime('%m/%d/%Y')
                    )
                ]]
            )
        )
    else:
        formatted_entries = [format_entry(entry) for entry in data]
        total_time = [0, 0]
        for time_entered in [x[1] for x in formatted_entries]:
            total_time[0] = total_time[0] + int(time_entered.split('h')[0])
            total_time[1] = total_time[1] + int(time_entered.split('h')[1])
        formatted_entries.append([
            '',
            '',
            '{:02d}h{:02d}'.format(*total_time),
            ''
        ])
        print('')
        print(tabulate(formatted_entries))
