# -*- coding: utf8 -*-
from weibo import APIClient
import urllib2
import urllib
 
def autoWeiboLogin(USERID, PASSWD):
    APP_KEY = '2190443373'
    APP_SECRET = '8d93d989f3ee23e821c4c84afd6cb54e'
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    #USERID = 'y.haohan@gmail.com'
    #PASSWD = 'AAbbCC99!!'
 
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    print "referer url is : %s" % referer_url
 
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
 
    postdata = {"client_id": APP_KEY,
             "redirect_uri": CALLBACK_URL,
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
                           url = AUTH_URL,
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

    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in

    client.set_access_token(access_token, expires_in)

    return client