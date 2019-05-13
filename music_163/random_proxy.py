#!/usr/bin/env python
# encoding: utf-8

"""
@description: 随机返回一个可用代理

@author: baoqiang
@time: 2019-05-09 19:59
"""

import random
import logging
import threading
import sys

proxies = []
lock = threading.Lock()
cookies = []


def init():
    global proxies
    with open('proxies_ok.txt', 'r', encoding='utf-8') as f:
        proxies = [line.strip() for line in f]
        logging.info('total proxy len: {}'.format(len(proxies)))

    global cookies
    with open('cookies.txt', 'r', encoding='utf-8') as f:
        cookies = [line.strip() for line in f]
        logging.info('total cookies len: {}'.format(len(cookies)))


def get_random_ip():
    """
    骗过反爬虫的终极解决方案！！！
    ！！！垃圾网易云！！！
    :return:
    """
    return '.'.join([str(int(''.join([str(random.randint(0, 2)), str(random.randint(0, 5)), str(random.randint(0, 5))]))) for _ in range(4)])


def get_random_cookie():
    return random.sample(cookies, 1)[0]


def get_random_proxy():
    # return random.sample(proxies, 1)[0]
    return ''

def get_random_proxy_lock():
    lock.acquire()

    if len(proxies) == 0:
        logging.error('proxy empty, exit')
        sys.exit(-2)

    result = random.sample(proxies, 1)[0]

    lock.release()

    return result


def remove_proxy(proxy):
    lock.acquire()

    if proxy in proxies:
        proxies.remove(proxy)
        logging.info("removing unavailable proxy[{}], now len: {}".format(proxy, len(proxies)))

    lock.release()


init()

if __name__ == '__main__':
    pass
