#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotGanji(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.url_pattern = re.compile(ur'^http://\w+\.ganji\.com(|/|/fang1/?|/fang1/\d+x\.htm|/fang1/tuiguang[-]\d+.htm|/fang1/f\d+/?)$', re.U | re.I)
        self.arch_pattern = re.compile(ur'[房户](\s|&nbsp;)*型[^：:]*[：:]([^\d]*)(\d[^<>\s]+)[\s<]', re.U | re.I)


    def get_address(self, page):
        ans = Robot.get_address(self, page)
        if ans == None:
            ans = Robot.get_district(self, page)

        return ans

    def is_valid_url(self, url):
        #print url
        ans = Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None and not url.startswith('http://www.ganji.com/fang1') and not url.startswith('http://help.ganji.com') and not url.startswith('http://club.ganji.com')
        #print ans
        return ans


#a = RobotGanji('http://www.ganji.com/index.htm', 'utf-8')
a = RobotGanji('http://gxyulin.ganji.com/fang1/', 'utf-8')
a.start()
