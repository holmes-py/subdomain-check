#!/usr/bin/python
# from tqdm import tqdm
import requests
import time
import os
from multiprocessing import Pool
import sys


ENDC = '\033[m'


def verifythis(i):
    url = f'https://{i}'
    session = requests.Session()
    resp = session.get(url, timeout=10)
    if '500' in str(resp):  # CYAN
        print(f'\033[0;37;46m{resp}' + ENDC, i)
    elif '302' in str(resp):  # YELLOW
        print(f'\033[0;37;43m{resp}' + ENDC, i)
    elif '301' in str(resp):  # YELLOW
        print(f'\033[0;37;43m{resp}' + ENDC, i)
    elif '200' in str(resp):  # GREEN
        print(f'\033[0;37;42m{resp}' + ENDC, i)
    elif "404" in str(resp):  # RED
        print(f'\033[0;37;41m{resp}' + ENDC, i)
    elif "403" in str(resp):  # BLUE
        print(f'\033[0;37;45m{resp}' + ENDC, i)
    elif '400' in str(resp):
        print(f'\033[0;37;48m{resp}' + ENDC, i)
    elif '500' or '404' or '200' or '302' or '301' or '403' or '400' not in str(resp):
        print(resp, i)

    # pbar.update(5)


def bufcount(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization
    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines


print('''
     _____         _     ____        _        ____ _     _
    |  ___|_ _ ___| |_  / ___| _   _| |__    / ___| |__ | | __
    | |_ / _` / __| __| \___ \| | | | '_ \  | |   | '_ \| |/ /
    |  _| (_| \__ \ |_   ___) | |_| | |_) | | |___| | | |   <
    |_|  \__,_|___/\__| |____/ \__,_|_.__/   \____|_| |_|_|\_/\

                                                   ~ MrHolmes''')
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('''
  Usage: ./SubdomainScan.py [filename]
  filename = Location of subdomains list.
  e.g.
  ./SubdomainScan.py /home/bugbounty/subdomains_of_tesla.txt
              ''')
    else:
        try:
            test = open(sys.argv[1])
            test.close()
        except FileNotFoundError:
            print('File not found. Retry.')
            exit()
        # tasks = range(5)
        start = time.time()
        pool = Pool(200)
        subdomainCount = bufcount(sys.argv[1])
        print(f'File provided: {sys.argv[1]}')
        print(f'Total Number of Subdomains to check: {subdomainCount}\n')
        # pbar = tqdm(total=subdomainCount)
        pool.imap_unordered(verifythis, [line.strip() for line in open(sys.argv[1], 'r')])
        pool.close()
        pool.join()
        end = time.time()
        print(f"\033[5;37;40m Time taken: {end-start} seconds.\033[0;37;40m" + ENDC)
        # pbar.close()
