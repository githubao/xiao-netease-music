#!/usr/bin/env python
# encoding: utf-8

"""
@description: 已经被封掉的ip

@author: baoqiang
@time: 2019-05-13 14:57
"""

black_file = 'black.txt'
fresh_file = 'fresh.txt'
proxy_file = 'proxies.txt'


def dup():
    with open(black_file, 'r') as f:
        black = set(line.strip() for line in f)

    with open(fresh_file, 'r') as f:
        fresh = set(line.strip() for line in f)

    # fresh里面有，black里面没有的
    left = fresh - black
    print('available: {}'.format(len(left)))

    with open(proxy_file, 'w') as fw:
        for item in left:
            fw.write('{}\n'.format(item))


def dup2():
    with open(fresh_file, 'r') as f:
        total = set(line.strip() for line in f)

    with open(proxy_file, 'w') as fw:
        for item in total:
            fw.write('{}\n'.format(item))


if __name__ == '__main__':
    # dup()
    dup2()
