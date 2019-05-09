"""
根据歌曲 ID 获得所有的歌曲所对应的评论信息
"""

import requests
from music_163 import sql
from xconcurrent import threadpool
import sys
import logging


class Comment(object):
    headers = {
        'Host': 'music.163.com',
        'Connection': 'keep-alive',
        'Content-Length': '484',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    params = {
        'csrf_token': ''
    }

    data = {
        'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
    }

    def save_comment(self, music_id):
        self.headers['Referer'] = 'http://music.163.com/playlist?id=' + str(music_id)

        r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                          headers=self.headers, params=self.params, data=self.data)
        resp = r.json()

        sql.insert_comments(music_id, resp['total'])

    def build_comments(self, dic):
        comments = dic.get('hotComments', [])
        return [item['content'] for item in comments]


class MultiComment(threadpool.MultiRun):
    my_comment = Comment()

    def run_one(self, dic):
        self.my_comment.save_comment(dic['id'])
        return dic


def multi_scrap_comment(batch_musics):
    # musics = sql.get_all_music()

    # 去重
    musics = set(item['MUSIC_ID'] for item in batch_musics)
    print('music len: {}'.format(len(musics)))

    tasks = [{"id": item} for item in musics]

    multi = MultiComment(tasks)
    multi.run_many()


def write_total(batch_musics):
    filename = '/Users/baoqiang/Downloads/music.txt'

    musics = set(item['MUSIC_ID'] for item in batch_musics)

    with open(filename, 'a', encoding="utf-8") as fw:
        for music in musics:
            fw.write('{}\n'.format(music))


def batch_multi_scrap_comment():
    total = 2856051
    batch_size = 1000

    for i in range(0, total, batch_size):
        logging.info('process cnt: {}'.format(i))
        rows = sql.get_batch_music(batch_size, i)
        multi_scrap_comment(rows)
        # write_total(rows)


def hello_comment():
    my_comment = Comment()

    my_comment.save_comment(440208476)


if __name__ == '__main__':
    batch_multi_scrap_comment()
    # hello_comment()
