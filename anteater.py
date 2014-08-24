#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################
# 27.11.2012 | word scraper bot wsb.py    #
# @pirate_security			  #
###########################################

import mechanize
import cookielib
import urllib2
from bs4 import BeautifulSoup
import re
import sys
import unicodedata
import os
import urlparse

# Ich bin ein Browser, bitte block mich nicht :_)
browser = mechanize.Browser()
cookies = cookielib.MozillaCookieJar('cookie_jar')
browser.set_cookiejar(cookies)
browser.set_handle_redirect(True)
browser.set_handle_robots(False)
browser.set_handle_equiv(True)
browser.set_handle_gzip(False)
browser.set_handle_referer(True)
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
browser.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:14.0) Gecko/20120405 Firefox/14.0a1')]

# Listen
linklist = []
wordlist = []

# Container
wordfile = open('wordlist.txt', 'w')
linkfile = open('links.txt', 'w')

# Koch die Suppe und Filter sie mir
initiallink = raw_input("enter target to scrape for words_> ")
linklist.append(initiallink)
print "scraping...  Press Ctrl+C to exit."

# Main Loop
###########

for link in linklist:
	try:
		soup = BeautifulSoup((browser.open(link)).read())
		filteredsoup = re.findall(r"(?:\s|^)(\w+)(?=\s|$)", ((soup.get_text()).encode('utf-8', 'ignore')))
		
		for word in filteredsoup:
			if (word not in wordlist) and (len(word) > 2 and len(word) < 12):
				wordlist.append(word)
				wordfile.write(str(word) + '\n')
				
		for eachnewlink in soup.findAll('a', href=True):
			eachnewlink['href'] = urlparse.urljoin(link, eachnewlink['href'])
			if eachnewlink not in linklist:
				linklist.append(eachnewlink['href'])
				linkfile.write(str(eachnewlink['href'].encode('utf-8', 'ignore')) + '\n')
	except:
		continue

