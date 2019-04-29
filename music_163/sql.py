"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors
from PyMysqlPool.connection import MySQLConnectionPool

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='00',
                             db='netease',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

config = {
    'pool_name': 'hello',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '00',
    'database': 'netease'
}

pool = MySQLConnectionPool(**config)


# 保存评论
def insert_comments(music_id, comment_cnt):
    conn = pool.borrow_connection()

    with conn.cursor() as cursor:
        sql = "INSERT INTO `comments` (`MUSIC_ID`, `COMMENT_CNT`) VALUES (%s, %s)"
        cursor.execute(sql, (music_id, comment_cnt))
    conn.commit()

    pool.return_connection(conn)


# 保存音乐
def insert_music(music_id, music_name, album_id):
    conn = pool.borrow_connection()

    with conn.cursor() as cursor:
        sql = "INSERT INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `ALBUM_ID`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (music_id, music_name, album_id))
    conn.commit()

    pool.return_connection(conn)


# 保存专辑
def insert_album(album_id, artist_id):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `albums` (`ALBUM_ID`, `ARTIST_ID`) VALUES (%s, %s)"
        cursor.execute(sql, (album_id, artist_id))
    connection.commit()


# 使用线程池
def insert_album2(album_id, artist_id):
    conn = pool.borrow_connection()

    with conn.cursor() as cursor:
        sql = "INSERT INTO `albums` (`ALBUM_ID`, `ARTIST_ID`) VALUES (%s, %s)"
        cursor.execute(sql, (album_id, artist_id))

    conn.commit()

    pool.return_connection(conn)


# 保存歌手
def insert_artist(artist_id, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (%s, %s)"
        cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY ARTIST_ID"
        # sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY RAND() limit 50"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有专辑的 ID
def get_all_album():
    with connection.cursor() as cursor:
        sql = "SELECT `ALBUM_ID` FROM `albums` ORDER BY ALBUM_ID"
        # sql = "SELECT `ALBUM_ID` FROM `albums` ORDER BY RAND() limit 200"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    with connection.cursor() as cursor:
        # sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY RAND() LIMIT 100"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取前一半音乐的 ID
def get_before_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 0, 800000"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取后一半音乐的 ID
def get_after_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 800000, 1197429"
        cursor.execute(sql, ())
        return cursor.fetchall()


def dis_connect():
    connection.close()
