#!/usr/bin/python

import urllib2
import json
import sys
import argparse

parser = argparse.ArgumentParser(description='Hangup/Answer Rest Call for Mobydick')

parser.add_argument('-u','--user',
                    help='sepcify the rest user', required=True)
parser.add_argument('-p','--password',
                    help='sepcify the password of the rest user', required=True)
parser.add_argument('-m','--mobydick',
                    help='sepcify the mobydick host adress', required=True)

args = vars(parser.parse_args())

user = args['user']
password = args['password']
url = 'http://' + args['mobydick'] + '/services/identity/states?keys=' + user
urlaction = 'http://' + args['mobydick'] + '/services/identity/' + user + '/defaultdevice/action'


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

