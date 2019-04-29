# xiao-netease-music
网易云音乐评论数量爬虫

copy from: https://github.com/RitterHou/music-163

![](https://img.shields.io/badge/Python-3.5.2-blue.svg)

这是一个爬取网易云音乐的所有的歌曲的评论数的爬虫。

### 以下为主要思路
1. 爬取所有的歌手信息（[artists.py](music_163/artists.py)）；
2. 根据上一步爬取到的歌手信息去爬取所有的专辑信息（[album_by_artist.py](music_163/album_by_artist.py)）；
3. 根据专辑信息爬取所有的歌曲信息（[music_by_album.py](music_163/music_by_album.py)）；
4. 根据歌曲信息爬取其评论条数（[comments_by_music.py](music_163/comments_by_music.py)）
5. 数据库相关的语句都存放于（[sql.py](music_163/sql.py)）中。


### 数据总数
1. artists.py: 去重之后有35069个歌手
http://music.163.com/discover/artist/cat?id=1001&initial=69
1. album_by_artist.py: 去重之后有370155张专辑
http://music.163.com/artist/album?id=1047211
1. music_by_album.py: 去重之后有首歌曲
http://music.163.com/album?id=1533948
