# xiao-netease-music
网易云音乐评论数量爬虫

copy from: https://github.com/RitterHou/music-163

![](https://img.shields.io/badge/Python-3.5.2-blue.svg)

这是一个爬取网易云音乐的所有的歌曲的评论数的爬虫。

### some tips
研究了代理池，随机cookie，最后发现在header里面加上一个随机的X-Real-IP字段: 
```python
from music_163 import random_proxy
headers = {'X-Real-IP': random_proxy.get_random_ip()}
```
就能够避免{"code": -460, "msg": "Cheating"}的错误了...累觉不爱

### 以下为主要思路
1. 爬取所有的歌手信息（[artists.py](music_163/artists.py)）；
2. 根据上一步爬取到的歌手信息去爬取所有的专辑信息（[album_by_artist.py](music_163/album_by_artist.py)）；
3. 根据专辑信息爬取所有的歌曲信息（[music_by_album.py](music_163/music_by_album.py)）；
4. 根据歌曲信息爬取其评论条数（[comments_by_music.py](music_163/comments_by_music.py)）
5. 数据库相关的语句都存放于（[sql.py](music_163/sql.py)）中


### 数据总数
1. artists.py: 去重之后有(35069)个歌手
http://music.163.com/discover/artist/cat?id=1001&initial=90
1. album_by_artist.py: 去重之后有(370155)张专辑
http://music.163.com/artist/album?id=6452
1. music_by_album.py: 去重之后有(2856051)首歌曲
http://music.163.com/album?id=18877
1. comments_by_music.py: 去重之后有(2856043)条评论
https://music.163.com/#/song?id=185709

### 收藏歌单
1. 评论大于5W的歌曲:  https://music.163.com/#/playlist?id=2792146274
1. 评论大于10W的歌曲: https://music.163.com/#/playlist?id=2792159323

### 代理ip
1. https://proxy.rudnkh.me/txt
1. https://proxyscrape.com/free-proxy-list
