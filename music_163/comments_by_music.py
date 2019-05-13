"""
根据歌曲 ID 获得所有的歌曲所对应的评论信息
"""

import requests
from music_163 import sql
from xconcurrent import threadpool
import sys
import logging
from music_163 import random_proxy
import datetime
import time
import random
import os

TRY_TIME = 10


class Comment(object):
    headers = {
        'Host': 'music.163.com',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '484',
        # 'Cache-Control': 'max-age=0',
        # 'Origin': 'http://music.163.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Accept': '*/*',
        # 'DNT': '1',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        # 'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    params = {
        'csrf_token': ''
    }

    data = {
        'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
    }

    def __init__(self):
        """
        NOTICE: 这样子定义的变量才是成员变量
        """
        self.success = 0
        self.failed = 0

    def save_comment(self, music_id):
        self.build_random_headers(music_id)

        r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                          headers=self.headers, params=self.params, data=self.data)
        resp = r.json()

        # save data
        if 'total' in resp:
            sql.insert_comments(music_id, resp['total'])
        else:
            logging.error('spider [{}] failed: {}'.format(music_id, resp))
            raise ValueError(music_id)

    def build_random_headers(self, music_id):
        self.headers['Referer'] = 'http://music.163.com/playlist?id=' + str(music_id)

        # cookie_fmt = 'JSESSIONID-WYYY={sid}%3A{now}; _iuqxldmzr_=25; _ntes_nnid={nid},{now}; _ntes_nuid={nid}; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'

        # now = int(time.time() * 1000)
        # sid = ua_mw.get_rand_sid()
        # nid = ua_mw.get_rand_nid()

        # self.headers['Cookie'] = cookie_fmt.format(now=now, sid=sid, nid=nid)
        # self.headers['User-Agent'] = ua_mw.get_rand_ua()

        # self.headers[
        #     'Cookie'] = 'MUSIC_U=e954e2600e0c1ecfadbd06b365a3950f2fbcf4e9ffcf7e2733a8dda4202263671b4513c5c9ddb66f1b44c7a29488a6fff4ade6dff45127b3e9fc49f25c8de500d8f960110ee0022abf122d59fa1ed6a2'

    def save_proxy_api_comment(self, music_id):
        ok = False

        for _ in range(TRY_TIME):
            proxy = random_proxy.get_random_proxy()
            try:
                self.save_api_comment(music_id, proxy)
                self.success += 1
                ok = True
                break
            except Exception as e:
                continue

        if not ok:
            self.failed += 1
            logging.error('spider id err: {}'.format(music_id))

    def save_api_comment(self, music_id, proxy):
        self.build_random_headers(music_id)

        # logging.info("use header: {}".format(self.headers))

        proxies = {
            'http': proxy
        }

        r = requests.post('http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(music_id),
                          headers=self.headers, proxies=proxies, timeout=0.5)
        resp = r.json()

        if 'total' in resp:
            sql.insert_comments(music_id, resp['total'])
        else:
            logging.error('spider [{}] failed: {}'.format(music_id, resp))
            raise ValueError(music_id)

    def build_comments(self, dic):
        comments = dic.get('hotComments', [])
        return [item['content'] for item in comments]


class MultiComment(threadpool.MultiRun):
    def __init__(self, tasks):
        super().__init__(tasks)
        self.my_comment = Comment()

    def run_one(self, dic):
        self.my_comment.save_proxy_api_comment(dic['id'])
        return dic

    def check_block(self):
        """
        查看有没有被封禁
        :return:
        """
        ok = self.my_comment.success
        fail = self.my_comment.failed

        logging.info('success: {}, failed: {}'.format(ok, fail))
        if fail / (ok + fail) > 0.5:
            logging.error('ok/fail:{}/{}, blocked'.format(ok, fail))
            sys.exit(-1)


def multi_scrap_comment(batch_musics):
    # musics = sql.get_all_music()

    # 去重
    musics = set(item['MUSIC_ID'] for item in batch_musics)
    logging.info('music len: {}'.format(len(musics)))

    tasks = [{"id": item} for item in musics]

    multi = MultiComment(tasks)
    multi.run_many()

    multi.check_block()


def write_total(batch_musics):
    filename = '/Users/baoqiang/Downloads/music.txt'

    musics = set(item['MUSIC_ID'] for item in batch_musics)

    with open(filename, 'a', encoding="utf-8") as fw:
        for music in musics:
            fw.write('{}\n'.format(music))


def batch_multi_scrap_comment():
    total = 2856051
    batch_size = 10000

    for i in range(0, total, batch_size):
        logging.info('process cnt: {}'.format(i))
        rows = sql.get_batch_music(batch_size, i)
        multi_scrap_comment(rows)
        # write_total(rows)


def batch_file_multi_scrap_comment():
    """
    从文件里面读取数据
    :return:
    """

    with open('/Users/baoqiang/Downloads/out.txt', 'r', encoding='utf-8') as f:
        datas = [{'MUSIC_ID': int(line.strip())} for line in f]

    batch_size = 5000
    istep = len(datas) // batch_size
    step = istep if len(datas) % batch_size == 0 else istep + 1
    for i in range(0, step):
        logging.info('process cnt: {}'.format(i * batch_size))
        batches = datas[batch_size * i: batch_size * (i + 1)]
        multi_scrap_comment(batches)
        # write_total(batches)


def batch_sample():
    """
    从文件里面读取数据
    :return:
    """
    datas = list(range(1, 17))
    batch_size = 3
    istep = len(datas) // batch_size
    step = istep if len(datas) % batch_size == 0 else istep + 1
    for i in range(0, step):
        print(datas[batch_size * i: batch_size * (i + 1)])


def hello_comment():
    my_comment = Comment()

    my_comment.save_proxy_api_comment(440208476)


if __name__ == '__main__':
    # batch_multi_scrap_comment()
    batch_file_multi_scrap_comment()
    # hello_comment()
