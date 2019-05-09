#!/usr/bin/env python
# encoding: utf-8

"""
@description: 并发检查proxy的可达性

@author: baoqiang
@time: 2019-05-09 19:43
"""

from xconcurrent import threadpool
import requests


class Proxy:
    def check(self, proxy):
        proxies = {
            'http': proxy
        }

        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_440208476'

        r = requests.post(url, proxies=proxies, timeout=0.5)
        resp = r.json()

        if 'total' in resp:
            print('RESULT:\t{}\t{}'.format(proxy, resp['total']))
        else:
            print('RESULT:\t{}\t{}'.format(proxy, -1))


class MultiComment(threadpool.MultiRun):
    proxy = Proxy()

    def run_one(self, dic):
        self.proxy.check(dic['proxy'])
        return dic


def multi_check():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.readlines()

    # 去重
    proxies = set(proxies)
    print('proxies len: {}'.format(len(proxies)))

    tasks = [{"proxy": item.strip()} for item in proxies]

    multi = MultiComment(tasks)
    multi.run_many()


if __name__ == '__main__':
    multi_check()
