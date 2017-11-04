# _*_ coding:utf-8 _*_
__author__ = 'tars'
_date__ = '2017/11/4 12:00'

import json


def initCookie(rconn, spiderName):
    pass


def load():
    try:
        with open('utils/cookie.json') as json_file:
            data = json.load(json_file)
            return data
    except IOError:
        print( "Error: 没有找到文件或读取文件失败")


def getCookie(userId):
    data = load()
    return data

# if __name__ == "__main__":
#     getCookie(1)