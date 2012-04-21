#encoding:utf-8
#Created by Liang Sun in 2012

import os, re, sys


from gevent import pool
from gevent import monkey
monkey.patch_all()


pattern = re.compile(r'^(\w+_bot)\.py$')
here = os.path.abspath(os.path.dirname(sys.argv[0]))
robots = []
for robot in os.listdir(here):
    m = pattern.match(robot)
    if m:
        robots.append(m.group(1))

def start_one(robot):
    print "Starting %s..." % robot
    module = __import__(robot)

request_pool = pool.Pool(len(robots))
for i in range(len(robots)):
    request_pool.spawn(start_one, robots[i])

request_pool.join()

