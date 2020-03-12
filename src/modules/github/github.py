#!/usr/bin/env python3

import time
from requests import get, post
from sys import stderr
import json
import os
from datetime import datetime
from pprint import pprint
from tabulate import tabulate
from multiprocessing import Pool
import shutil

script_directory = os.path.dirname(os.path.realpath(__file__))
index_files_directory = '{}/.git_indexes'.format(script_directory)
token_location = '{}/security/.token'.format(script_directory)
octo_arm_location = '{}/.octo_arm'.format(script_directory)

try:
    with open(token_location, 'r') as f:
        token = f.read().strip()

    assert len(token) > 0
except Exception as e:
    print('''A github personal access token (https://github.com/settings/tokens) stored in '~/.conky/src/modules/github/security/.token' with the following permissions is required:
        * read:user
        * notifications
        * repo''', file=stderr)


def get_arm_position():
    try:
        with open(octo_arm_location, 'r') as f:
            arm_position = int(f.read())
    except Exception:
        arm_position = 0
    else:
        os.remove(octo_arm_location)
    finally:
        with open(octo_arm_location, 'w') as f:
            if (arm_position == 0):
                f.write('1')
            if (arm_position == 1):
                f.write('2')
            if (arm_position == 2):
                f.write('3')
            if (arm_position == 3):
                f.write('0')

    return arm_position


def write_index_file(pair):
    with open('{}/{}.url'.format(index_files_directory, pair[0]), 'w+') as f:
        f.write(pair[1])


def write_urls_to_files(index_url_pairs):
    try:
        shutil.rmtree(index_files_directory)
    except Exception as e:
        pass

    os.mkdir(index_files_directory)

    with Pool() as p:
        p.map(write_index_file, index_url_pairs)


def prettydate(d):
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(int(s/60))
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(int(s/3600))


def query(body='{}', api_url='https://api.github.com/graphql', method=post):
    return method(url=api_url, headers={
        'Authorization': 'bearer {}'.format(token),
        'Content-Type': 'application/json'
    }, data=json.dumps({'query': body})).json()['data']['viewer']['login']


def get_github_user():
    return query('''query {
            viewer {
                login
            }
        }''')


def get_notifications():
    for notification in get('https://api.github.com/notifications?access_token={}&page=1&per_page=9&unread=1+sort:updated_at-desc'.format(token)).json():
        # pprint(notification, indent=4)
        yield {
            'updated_at': prettydate(datetime.strptime(notification['updated_at'], '%Y-%m-%dT%H:%M:%SZ')),
            'repository': '{}'.format(notification['repository']['full_name']),
            'title': notification['subject']['title'][:48],
            'type': notification['subject']['type'],
            'id': notification['subject']['url'].split('/')[-1],
        }


def display_octocat(user, tabs):
    added_lines = []

    for tab in tabs[:15]:
        added_lines.append(tab)

    while len(added_lines) < 15:
        added_lines.append('')

    arm_position = get_arm_position()
    if arm_position == 0:
        print('''
           MMM.           .MMM
           MMMMMMMMMMMMMMMMMMM              🤖  Hi there {}
           MMMMMMMMMMMMMMMMMMM
          MMMMMMMMMMMMMMMMMMMMM             {}
         MMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMM::- -:::::::- -::MMMM           {}
         MM~:~   ~:::::~   ~:~MM            {}
    .. MMMMM::. .:::+:::. .::MMMMM ..       {}
          .MM::::: ._. :::::MM.             {}
             MMMM;:::::;MMMM                {}
      -MM        MMMMMMM                    {}
      ^  M+     MMMMMMMMM                   {}
          MMMMMMM MM MM MM                  {}
               MM MM MM MM                  {}
               MM MM MM MM                  {}
            .~~MM~MM~MM~MM~~.               {}
         ~~~~MM:~MM~~~MM~:MM~~~~            {}
        ~~~~~~==~==~~~==~==~~~~~~
         ~~~~~~==~==~==~==~~~~~~            What one programmer can do in one month, two programmers can do in two months.
             :~==~==~==~==~~)
'''.format(user, *added_lines))
    elif arm_position == 1 or arm_position == 3:
        print('''
           MMM.           .MMM
           MMMMMMMMMMMMMMMMMMM              🤖  Hi there {}
           MMMMMMMMMMMMMMMMMMM
          MMMMMMMMMMMMMMMMMMMMM             {}
         MMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMM::- -:::::::- -::MMMM           {}
         MM~:~   ~:::::~   ~:~MM            {}
    .. MMMMM::. .:::+:::. .::MMMMM ..       {}
          .MM::::: ._. :::::MM.             {}
             MMMM;:::::;MMMM                {}
                 MMMMMMM                    {}
                MMMMMMMMM                   {}
     ^MMMMMMMMMMM MM MM MM                  {}
               MM MM MM MM                  {}
               MM MM MM MM                  {}
            .~~MM~MM~MM~MM~~.               {}
         ~~~~MM:~MM~~~MM~:MM~~~~            {}
        ~~~~~~==~==~~~==~==~~~~~~
         ~~~~~~==~==~==~==~~~~~~            What one programmer can do in one month, two programmers can do in two months.
             :~==~==~==~==~~)
'''.format(user, *added_lines))
    elif arm_position == 2:
        print('''
           MMM.           .MMM
           MMMMMMMMMMMMMMMMMMM              🤖  Hi there {}
           MMMMMMMMMMMMMMMMMMM
          MMMMMMMMMMMMMMMMMMMMM             {}
         MMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMMMMMMMMMMMMMMMMMMMMMM            {}
        MMMM::- -:::::::- -::MMMM           {}
         MM~:~   ~:::::~   ~:~MM            {}
    .. MMMMM::. .:::+:::. .::MMMMM ..       {}
          .MM::::: ._. :::::MM.             {}
             MMMM;:::::;MMMM                {}
                 MMMMMMM                    {}
                MMMMMMMMM                   {}
          MMMMMMM MM MM MM                  {}
         M+    MM MM MM MM                  {}
     ^-MM      MM MM MM MM                  {}
            .~~MM~MM~MM~MM~~.               {}
         ~~~~MM:~MM~~~MM~:MM~~~~            {}
        ~~~~~~==~==~~~==~==~~~~~~
         ~~~~~~==~==~==~==~~~~~~            What one programmer can do in one month, two programmers can do in two months.
             :~==~==~==~==~~)
'''.format(user, *added_lines))


if __name__ == '__main__':
    user = get_github_user()

    tabs = []
    index_url_pairs = []

    for index, notification in enumerate(get_notifications()):
        if notification['type'] == 'Issue':
            notification_icon = 'Issue'
        else:
            notification_icon = 'PR'
        tabs.append(['[Ctrl+G+{}]'.format(index + 1), notification_icon, notification['updated_at'], notification['repository'],
                     notification['title']])
        index_url_pairs.append([
            index + 1,
            'https://github.com/{}/{}/{}'.format(
                notification['repository'], 'issues' if notification['type'] else 'pulls', notification['id'])
        ])
    write_urls_to_files(index_url_pairs)
    display_octocat(user, tabulate(tabs).splitlines())
