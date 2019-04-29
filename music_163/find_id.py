#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爬取失败的id

@author: baoqiang
@time: 2019-04-29 17:37
"""

import re

pat = re.compile('{\'id\': ([\\d]+)}')


def run():
    exists = set()

    with open('1.txt', 'r', encoding='utf-8') as f:
        for line in f:
            m = pat.search(line)
            exists.add(m.group(1))

    print('\n'.join(exists))


if __name__ == '__main__':
    run()
