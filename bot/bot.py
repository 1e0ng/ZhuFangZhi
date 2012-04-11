#encoding:utf-8
#Created by Liang Sun in 2012

#Crawl http://anjuke.com only for this version


import re
import urllib
import robotexclusionrulesparser

class ZfzURLopener(urllib.FancyURLopener):
    version = "Zfz-bot/1.0"

urllib._urlopener = ZfzURLopener()

def explore(url):



def insite_search(root):
    rerp = robotexclusionrulesparser.RobotExclusionRulesParser()
    rerp.user_agent = "Zfz-bot/1.0"
    try:
        rerp.fetch(root + "/robots.txt")
    except:
        pass

    open = [root]
    close = set()

    while len(open) > 0:
        url = open.pop()
        if not rerp.is_allowed('*', url):
            continue

        close.add(url)
        page = explore(url)


    #rerp.is_allowed('*', url)



seeds = ['http://beijing.anjuke.com',
        'http://zufang.sina.com.cn',
        'http://bj.ganji.com',
        'http://bj.58.com/zufang/',
        'http://haozu.com']

#root = 'http://zhufangzhi.com'


