#!/usr/bin/env python
# encoding: utf-8

"""
@description: 随机返回一个可用代理

@author: baoqiang
@time: 2019-05-09 19:59
"""

import random

proxies = []


def init():
    global proxies
    with open('proxies_ok.txt', 'r', encoding='utf-8') as f:
        proxies = [line.strip() for line in f]


def get_random_proxy():
    return random.sample(proxies, 1)[0]


init()

if __name__ == '__main__':
    pass
