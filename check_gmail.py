#!/usr/bin/python
import keyring
import subprocess
import getpass
import sys
import os
import time
from xml.dom.minidom import parseString

uname = sys.argv[1]
cache_file_name = os.path.expanduser('~/scripts/last_gmail_%s' % uname)
timeout = 300 # in seconds
if os.access(cache_file_name, os.R_OK):
	cache_file = open(cache_file_name, 'r')
	# check the last modified time
	statinfo = os.stat(cache_file_name)
	if time.time() - statinfo.st_mtime < timeout:
		cval = cache_file.read()
		if cval != "":
			print cval
			sys.exit(0)
cache_file = open(cache_file_name, 'w')

try:
	pw = keyring.get_password('check_gmail', uname)
	if pw == None:
		pw = getpass.getpass()
		keyring.set_password('check_gmail', uname, pw)
	res = subprocess.check_output(['curl', '-su', '%s:%s' % (uname, pw), 'https://mail.google.com/mail/feed/atom'])
	dom = parseString(res)
	unread_count_elem = dom.getElementsByTagName('fullcount')[0]
	unread_count = "".join([td.data for td in unread_count_elem.childNodes if td.nodeType == td.TEXT_NODE])
	print unread_count
	cache_file.write(unread_count)
	cache_file.close()
except:
	print "err"
