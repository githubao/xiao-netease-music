#!/usr/bin/env python
# encoding: utf-8

"""
@description: comment

@author: baoqiang
@time: 2019-05-09 18:23
"""

import requests
from scrapy.selector import Selector


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


if __name__ == '__main__':
    # spider_comment()
    static_var()
