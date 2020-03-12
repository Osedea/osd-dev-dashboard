#!/usr/bin/env python3
import subprocess
import nmap
import math
from tabulate import tabulate
nmapscan = nmap.PortScanner()

def go():
    nmapscan.scan(hosts='192.168.1.0/24', arguments='-sn')

    hosts = generate_host(nmapscan.all_hosts())
    print_content(hosts)

def generate_host(all_hosts):
    addresses = []
    for host in all_hosts:
        hostname = nmapscan[host].hostname()
        if '.localdomain' in hostname:
            hostname = hostname[0:hostname.index('.localdomain')]
        addresses.append({
            "hostname": hostname,
            "ip": host,
            "status": nmapscan[host].state()
        })
    return addresses


def print_content(c):
    x = list(chunk(c, 5))
    for hosts in x:
        line1 = ''
        line2 = ''
        for host in hosts:
            line1 = line1 + format(host["hostname"])
            line2 = line2 + format(host["ip"])
        print(line1)
        print(line2 + '\n')

def chunk(l, n):
    for i in range(0, len(l),n):
        yield l[i:i + n]
    
def format(s):
    s = (s[:15] + '...') if len(s) > 15 else s
    return s.ljust(20,' ')

if __name__ == "__main__":
    go()