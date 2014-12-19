import sys
import urllib2
import json
from time import sleep

_timeout_count = 0
_timeouts = [60, 300, 600, 1800, 3600] #1min, 5mins, 10mins, 30mins, 60mins

def timeout(_timeout_count, _timeouts):
    if _timeout_count > len(_timeouts):
        print '\nTimeouts have exceeded max number. Exiting!'
        sys.exit()
    else:
        print '\nTimeout! Waiting', str(_timeouts[_timeout_count] / 60), 'minute(s) before resuming...'
        sleep(_timeouts[_timeout_count])

swipe_rate = 0.5 #Delay time in seconds
facebook_token = '***FACEBOOK TOKEN***' #I had to use Charles Proxy to intercept the Tinder app packet from my phone with this in
facebook_id = '***FACEBOOK ID***'

loginCredentials = {
                    'facebook_token': facebook_token, 
                    'facebook_id': facebook_id
                   }

headers_auth = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept-Language': 'fr;q=1, en;q=0.9, de;q=0.8, zh-Hans;q=0.7, zh-Hant;q=0.6, ja;q=0.5',
            'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
            'os_version': '700001',
            'Accept': '*/*',
            'platform': 'ios',
            'Connection': 'keep-alive',
            'app_version': '3',
            'Accept-Encoding': 'gzip, deflate'
          }
print "\n*** Tinder-Py Auto Liker ***"
print '\nAuthenticating...'

r_auth = urllib2.Request('https://api.gotinder.com/auth', data=json.dumps(loginCredentials), headers=headers_auth)
resp_auth = json.loads(urllib2.urlopen(r_auth).read())
x_auth_token = resp_auth['token']
myname = resp_auth['user']['full_name']

print '\nAuthenticated as', myname

header = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)',
            'X-Auth-Token' : x_auth_token
          }

print '\nLiking users...\n'

counter = 0
while True:
    respDebug = None
    try:
        r_recs = urllib2.Request('https://api.gotinder.com/user/recs', headers=header)
        resp_recs = json.loads(urllib2.urlopen(r_recs).read())
        respDebug = resp_recs
        if 'message' in resp_recs:
            if resp_recs['message'] == 'recs exhausted':
                print '\nThere is noone new around you!'
                timeout(_timeout_count, _timeouts)
                _timeout_count += 1
                continue
            if resp_recs['message'] == 'recs timeout':
                print '\nError! Connection Timeout'
                timeout(_timeout_count, _timeouts)
                _timeout_count += 1
                continue

        hoes = resp_recs['results']
        for hoe in hoes:
            sleep(swipe_rate)
            _id = hoe['_id']
            r_like =  urllib2.Request('https://api.gotinder.com/like/' + _id, headers=header)
            status = json.loads(urllib2.urlopen(r_like).read())['match']
            if status:
                print '\nMatched with:', hoe['name']
            _timeout_count = 0
            counter += 1
            sys.stdout.write('\rLiked user count: ' + str(counter))
            sys.stdout.flush()
    except:
        print '\nError!'
        print respDebug