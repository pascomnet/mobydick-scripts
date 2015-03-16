#!/usr/bin/python

import urllib2
import json
import sys

url = 'http://127.0.0.1/services/voicemailbox/' + sys.argv[1]

opener = urllib2.build_opener()
urllib2.install_opener(opener)

data = json.loads(urllib2.urlopen(url).read())

print data['016voi_email']
