#!/usr/bin/python

import urllib2
import json
import sys
import configparser

config = configparser.ConfigParser()

try:
    config.read_file(open('/Users/tmattausch/work/conf/rest.conf'))
except IOError:
    print "ERR: configuration file could not be found"
    sys.exit(3)

try:
    user = config.get('REST','user')
    password = config.get('REST','password')
    mobydick = config.get('REST','host')
except:
    print "ERR in config"
    sys.exit(3)

url = 'http://' + mobydick + '/services/identity/states?keys=' + user
urlaction = 'http://' + mobydick + '/services/identity/' + user + '/defaultdevice/action'

password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(
    None, url, user, password
)
password_manager.add_password(
    None, urlaction, user, password
)
auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

checkstate = json.loads(urllib2.urlopen(url).read())

print checkstate[user]['state']

def sendaction(type):
    postdata = {'action':type}
    req = urllib2.Request(urlaction)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(postdata))

if checkstate[user]['state'] == 'Ringing':
    sendaction('offhook')
    sys.exit(0)
elif checkstate[user]['state'] == 'InUse':
    sendaction('hangup')
    sys.exit(0)
else:
    print 'Nothing to do'
    sys.exit(0)

