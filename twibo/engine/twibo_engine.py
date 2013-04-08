# -*- coding: utf8 -*-
# Twibo Engine for Twitter -> Weibo reposting
# By Alfred Yuan, UC Berkeley
# All Copyrights Reserved.

# Weibo Auto Login
# import requests
import json
import sys
import requests

sys.path.append('..')

from sqlalchemy import create_engine
import transaction

from models import (
	DBSession,
	Customer,
	Base,
	Tweet,
	Weibo,
	TwiboEngineLog
	)

from datetime import datetime

import time

import twitter
import weibo
from weibo import APIClient
import urllib2
import urllib
import re

class TwiboDataStream:
	def __init__():
		pass

class TwitterParser:
	ShortLinkUrl = 'http://api.longurl.org/v2/expand'

	@staticmethod
	def ShortLink(source):
		r=requests.get(TwitterParser.ShortLinkUrl, params={'url':source,'format':'json'})
		return json.loads(r.text)['long-url']

	@staticmethod
	def process(source):
		# location urls
		urls = re.findall(r'(https?://\S+)', source)

		for url in urls:
			source = re.sub(url, TwitterParser.ShortLink(url), source, count=1)

		return source

class TwiboEngine:	
	DatabaseUrl = 'mysql://root:password@localhost/twibo_db?charset=utf8'
	#DatabaseUrl = 'mysql://alfredyuan:AAbbCC99!!@localhost/twibo_db?charset=utf8'
	SLEEP_TIME = 1800
	RECENT_RETRIEVE = 30

	# Twitter Configuration
	tw_consumer_key = "gGlhtxpw1nW5gDwbPJnU4w"
	tw_consumer_secret = "jWmeFahHQzi6pOjBsjkBY0cEmK7GpolpPYta06FS0i4"
	tw_access_token = "16324190-IgS3RBr7YAWEYrMgwOI1MAjLVKFe1EwPdGNg8P5Dh"
	tw_access_token_secret = "D3XrT4ZedLc852IH2M1sJl0onuKMDJqF79iRO8I"

	# Weibo Configuration
	APP_KEY = '2190443373'
	APP_SECRET = '8d93d989f3ee23e821c4c84afd6cb54e'
	CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
	AUTH_URL = 'https://api.weibo.com/oauth2/authorize'

	def __initDBSession(self):
		self.engine = create_engine(self.DatabaseUrl)
		DBSession.configure(bind = self.engine)
		Base.metadata.bind = self.engine

	def __init__(self):
		# initialize database
		self.__initDBSession()

	def __del__(self):
		print "SHUTDOWN"

	def __log(self, top_log, customer_id=None, sec_log=None, detail_log=None):
		print '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'] ' + top_log + ' ' + str(customer_id) + ' ' + str(sec_log) + ' ' + str(detail_log)
		with transaction.manager:
			l = TwiboEngineLog(top_log, customer_id, sec_log, detail_log)
			DBSession.add(l)

	def run(self):
		# Infinite loop machine
		self.__log('START')

		self.process()
		self.__log('WAIT',None, str(self.SLEEP_TIME/60)+' mins')
		#time.sleep(self.SLEEP_TIME)

	@staticmethod
	def getTwitterHandler():
		return twitter.Api(consumer_key=TwiboEngine.tw_consumer_key,consumer_secret=TwiboEngine.tw_consumer_secret,access_token_key=TwiboEngine.tw_access_token, access_token_secret=TwiboEngine.tw_access_token_secret)

	@staticmethod
	def getWeiboHandler(USERID, PASSWD):
	    client = APIClient(app_key=TwiboEngine.APP_KEY, app_secret=TwiboEngine.APP_SECRET, redirect_uri=TwiboEngine.CALLBACK_URL)
	    referer_url = client.get_authorize_url()
	    print "referer url is : %s" % referer_url
	 
	    cookies = urllib2.HTTPCookieProcessor()
	    opener = urllib2.build_opener(cookies)
	    urllib2.install_opener(opener)
	 
	    postdata = {"client_id": TwiboEngine.APP_KEY,
	             "redirect_uri": TwiboEngine.CALLBACK_URL,
	             "userId": USERID,
	             "passwd": PASSWD,
	             "isLoginSina": "0",
	             "action": "submit",
	             "response_type": "code",
	             }
	 
	    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
	               "Host": "api.weibo.com",
	               "Referer": referer_url
	             }
	 
	    req  = urllib2.Request(
	                           url = TwiboEngine.AUTH_URL,
	                           data = urllib.urlencode(postdata),
	                           headers = headers
	                           )
	    try:
	        resp = urllib2.urlopen(req)
	        print "callback url is : %s" % resp.geturl()
	        print "code is : %s" % resp.geturl()[-32:]
	    except Exception, e:
	        print e

	    code = resp.geturl()[-32:]

	    try:
	    	r = client.request_access_token(code)
	    except weibo.APIError:
	    	return None

	    access_token = r.access_token
	    expires_in = r.expires_in

	    client.set_access_token(access_token, expires_in)

	    return client

	@staticmethod
	def getTwitterTimelineByUserId(apiHandler, user_id, count=0):
		return apiHandler.GetUserTimeline(user_id, count = count)

	@staticmethod
	def getNewTweetsByUserId(apiHandler, user_id):
		# Fetch recent 200 tweets
		t_ = TwiboEngine.getTwitterTimelineByUserId(apiHandler, user_id, count = TwiboEngine.RECENT_RETRIEVE)

		t_.reverse()

		for i, t in enumerate(t_):
			if not DBSession.query(Tweet).filter_by(twitter_id=str(t.id)).all():
				break
			if i==len(t_)-1:
				i = len(t_)

		return t_[i:]


	def process(self):
		# Process Twitter -> Weibo
		self.__log('START_PROCESSING')

		c_ = DBSession.query(Customer).all()

		# obtain twitter handler
		api = TwiboEngine.getTwitterHandler()

		if not api:
			self.__log('TWITTER_API_ERROR' )
			return

		for c in c_:
			self.__log('START_PROCESSING_CUSTOMER', c.id )

			# load tweets
			t_ = TwiboEngine.getNewTweetsByUserId(api, c.tw_name)

			t_set = list()
			#w_set = list()

			for t in t_:
				new_t = Tweet(t, c.id)
				self.__log('NEW_TWEET', c.id, str(t.id), t.text.encode('utf-8'))
				t_set.append(new_t)

			with transaction.manager:
				DBSession.add_all(t_set)
				#DBSession.add_all(w_set)

			self.__log('NEW_TWEETS_LOADED', c.id)

			# Login Weibo
			if c.wi_account_name.strip() is not '' and c.wi_account_pwd.strip() is not '':
				weibo_client = TwiboEngine.getWeiboHandler(c.wi_account_name, c.wi_account_pwd)
			else:
				weibo_client = None

			if not weibo_client:
				self.__log('WRONG_WEIBO_ACCOUNT', c.id, None,'NO WEIBO ACCOUNT for Customer '+str(c.tw_name)+', Auto Sync would be turned off')
				if c.auto_sync:
					c.auto_sync = False
					DBSession.commit()
				continue				

			w_set = list()

			for t in c.tweets:
				if not t.Weibo:
					try:
						w = weibo_client.statuses.update.post(status = TwitterParser.process(t.text).encode('utf-8'))
					except weibo.APIError:
						w = None

					if w:
						w_set.append(Weibo(w, t.id, c.id))
						self.__log('NEW_WEIBO', c.id, str(w.id), w.text.encode('utf-8'))
					else:
						self.__log('WRONG_POST_WEIBO', c.id, str(t.id) )

			with transaction.manager:
					DBSession.add_all(w_set)

			self.__log('WEIBO_SYNDICATED', c.id)

			self.__log('END_PROCESSING_CUSTOMER', c.id )

		self.__log('END_PROCESSING')

			
if __name__ == '__main__':
	engine = TwiboEngine()

	engine.run()
