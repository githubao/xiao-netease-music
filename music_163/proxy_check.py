#!/usr/bin/env python
# encoding: utf-8

"""
@description: 并发检查proxy的可达性

@author: baoqiang
@time: 2019-05-09 19:43
"""

from xconcurrent import threadpool
import requests
import logging
from collections import defaultdict
from music_163 import random_proxy

outfile = 'proxies_ok.txt'
TRY_TIME = 5


class Proxy:

    def __init__(self):
        self.results = []

    def check(self, proxy):
        proxies = {
            'http': proxy
        }

        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_440208476'

        headers = {
            'Cookie': random_proxy.get_random_cookie()
        }

        r = requests.post(url, proxies=proxies, headers=headers, timeout=2)
        resp = r.json()

        if 'total' in resp:
            # print('RESULT:\t{}\t{}'.format(proxy, resp['total']))
            if resp['total'] > 1000:
                self.results.append(proxy)

        else:
            logging.info('RESULT:\t{}\t{}'.format(proxy, -1))


class MultiComment(threadpool.MultiRun):

    def __init__(self, tasks):
        super().__init__(tasks)
        self.proxy = Proxy()

    def run_one(self, dic):
        try:
            self.proxy.check(dic['proxy'])
            return dic
        except Exception as e:
            return None

    def write_file(self):
        with open(outfile, 'a', encoding='utf-8') as fw:
            for line in self.proxy.results:
                fw.write('{}\n'.format(line))


def multi_check():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.readlines()

    # 去重
    proxies = set(proxies)
    print('proxies len: {}'.format(len(proxies)))

    tasks = [{"proxy": item.strip()} for item in proxies]

    multi = MultiComment(tasks)
    multi.run_many()

    multi.write_file()


def many_multi_check():
    """
    跑三次数据，两次以上的才可用
    :return:
    """
    for i in range(TRY_TIME):
        multi_check()
        logging.info('process time complete: {}'.format(i + 1))


if __name__ == '__main__':
    many_multi_check()
