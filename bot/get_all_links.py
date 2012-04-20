#encoding:utf-8
#Created by Liang Sun in 2012

import re
import sys
import codecs

page = codecs.open('in.html', 'r', 'utf-8').read()
link_pattern = re.compile(r'\s+href="([^\s\'">]+)"[\s>]', re.U | re.I)
url_pattern = re.compile(ur'^http://\w+.baixing.com(|/|fang/?|/zhengzu/?|/zhengzu/[\w\d]+\.html)$')
all_links = link_pattern.findall(page)
all_links = list(set(all_links))
fo = codecs.open('out', 'w', 'utf-8')
for link in all_links:
    if link.find('?') == -1 and url_pattern.match(link) != None:
        fo.write('<a href="' + link + '">' + link + '</a>\n')

fo.close()
