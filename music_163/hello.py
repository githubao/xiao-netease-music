#!/usr/bin/env python
# encoding: utf-8

"""
@description: comment

@author: baoqiang
@time: 2019-05-09 18:23
"""

import requests
from scrapy.selector import Selector
import logging
from music_163 import random_proxy


class A:
    other = 0

    def __init__(self):
        self.cnt = 0

    def add(self):
        self.cnt += 1
        self.other += 1


def static_var():
    a1 = A()
    a1.add()

    a2 = A()
    a2.add()

    print(a2.cnt)
    print(a2.other)


def spider_comment():
    url = 'https://music.163.com/song?id=185709'
    resp = requests.get(url)
    root = Selector(text=resp.content)
    comment_url = root.xpath('.//div[@id="comment-box"]//h3//span[@class="j-flag"]/text()')

    if comment_url:
        print(int(comment_url[0].extract().strip()))
    else:
        print('not found')


def spider_using_cookie():
    # with open('cookies.txt', 'r', encoding='utf-8') as f:
    #     for line in f:
    #         line = line.strip()
    #
    #         headers = {
    #             'Cookie': line
    #         }

    with open('proxies_ok.txt', 'r', encoding='utf-8') as g:
        for gline in g:
            proxies = {'http': gline.strip()}
            try:
                r = requests.post(url, headers={}, proxies=proxies, timeout=2)
                print(r.json())
            except Exception as e:
                logging.error(e)


url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_440208476'


def spider_using_cookie2():
    # headers = {'Cookie': random_proxy.get_random_cookie()}
    # proxies = {'http':random_proxy.get_random_proxy()}

    # proxies = {'http': '123.58.9.79:8080'}

    proxies = {}
    headers = {}
    # ip = random_proxy.get_random_ip()
    # print(ip)
    # headers = {'X-Real-IP': ip}

    r = requests.post(url, headers=headers, proxies=proxies, timeout=2)
    print(r.json())


if __name__ == '__main__':
    # spider_comment()
    # static_var()
    spider_using_cookie2()
