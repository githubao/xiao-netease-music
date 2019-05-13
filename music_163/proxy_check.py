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

outfile = 'proxies_ok.txt'
TRY_TIME = 5


class Proxy:
    results = []

    def check(self, proxy):
        proxies = {
            'http': proxy
        }

        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_440208476'

        r = requests.post(url, proxies=proxies, timeout=0.5)
        resp = r.json()

        if 'total' in resp:
            # print('RESULT:\t{}\t{}'.format(proxy, resp['total']))
            if resp['total'] > 1000:
                self.results.append(proxy)

        else:
            logging.info('RESULT:\t{}\t{}'.format(proxy, -1))


class MultiComment(threadpool.MultiRun):
    proxy = Proxy()

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


def count_sum():
    dic = defaultdict(int)

    with open(outfile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            dic[line] += 1

    sorted_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    for item, count in sorted_list:
        # print(item, count)
        pass
    for item, count in sorted_list:
        if count <= 5:
            break

        print(item)


if __name__ == '__main__':
    # many_multi_check()
    count_sum()
