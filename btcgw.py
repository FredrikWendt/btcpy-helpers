#!/usr/bin/env python
#
# A quick hack that logs in to btcguild.com and withdraws all available funds
# modify username and password at the bottom and you should be all set.
#
# Licence: GPLv2
# 
# Feel like thanking? A donation to 1BF4HMQvqmoobo2FtVYVTy2HZv8W2FwvNe is welcome. :)
#

import mechanize

URL_LOGIN = 'https://www.btcguild.com/my_account.php'
DEBUG = False

def log(*args):
	if DEBUG:
		print(args)


def select_pay_me_now_form(f):
	for c in f.controls:
		log(c.type, c.name)
		if c.type == 'hidden' and c.name == 'secret_token':
			log(True)
			return True
	return False

def select_login_form(f):
	for c in f.controls:
		log(c.type, c.name)
		if c.type == 'password' and c.name == 'password':
			log(True)
			return True
	return False


def pay_me_now(username, password):
	if DEBUG:
		import sys, logging
		logger = logging.getLogger("mechanize")
		logger.addHandler(logging.StreamHandler(sys.stdout))
		logger.setLevel(logging.DEBUG)

	cookies = mechanize.CookieJar()
	opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
	opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; BTCGPayOut/0.1)")]
	mechanize.install_opener(opener)

	br = mechanize.Browser()
	if DEBUG:
		br.set_debug_http(True)
		br.set_debug_responses(True)
		br.set_debug_redirects(True)

	br.set_handle_robots(False)

	# login
	try:
		br.open(URL_LOGIN)
		br.select_form(predicate=select_login_form)
		br['username'] = username
		br['password'] = password
		br.submit()
		br.select_form(predicate=select_pay_me_now_form)
	except:
		print "Failed to login"
		return

	# click my_account, but with nonce/secret_token being empty
	br.reload()

	# logged in
	try:
		br.select_form(predicate=select_pay_me_now_form)
	except:
		print "Failed to find withdraw form"
		return

	br.submit()


if __name__ == '__main__':
	import sys
	if not len(sys.argv) == 3:
		print "Missing username and password: python %s user pass" % (sys.argv[0])
		sys.exit(1)
	pay_me_now(sys.argv[1], sys.argv[2])
