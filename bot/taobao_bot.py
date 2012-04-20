#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotTaobao(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.price_pattern = re.compile(ur'租(\s|&nbsp;)*金[^：:]*[：:]\s*(<[^<>]+>\s*)*(\d+)\s*<', re.U | re.I)
        self.url_pattern = re.compile(ur'^http://fang.taobao.com(|/|/\w+/r/[\w\d]+\.html|\w+/zufang/?|/city/cityjumpnew.html\?.*)$', re.U | re.I)

    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = RobotTaobao('http://fang.taobao.com/city/changecity.html?city=99&channel=rentout&subChannel=&back=0', 'gbk')
a.start()
