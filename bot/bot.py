#encoding:utf-8
#Created by Liang Sun in 2012

#Crawl http://anjuke.com only for this version


import re
import robotexclusionrulesparser

root = 'http://beijing.anjuke.com'
rerp = robotexclusionrulesparser.RobotExclusionRulesParser()

# I'll set the (optional) user_agent before calling fetch.
rerp.user_agent = "ZhuFangZhi-bot/1.0"

# Note that there should be a try/except here to handle urllib2.URLError,
# socket.timeout, UnicodeError, etc.
try:
    rerp.fetch(root + "/robots.txt")
except:
    return True

#for user_agent, url in user_agents_and_urls:
#    print "Can %s fetch '%s'? %s" % \
#          (user_agent, url, rerp.is_allowed(user_agent, url))

#rp = robotparser.RobotFileParser()
#rp.set_url(root + '/robots.txt')
#rp.read()
print rerp.is_allowed('*', root + '/rental/')
print rerp.is_allowed('*', root + '/include/')
print rerp.is_allowed('*', root + '/tycoonsearch.php')

#rp = robotparser.RobotFileParser()
#rp.set_url("http://www.musi-cal.com/robots.txt")
#rp.read()
#print rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
#print rp.can_fetch("*", "http://www.musi-cal.com/")

