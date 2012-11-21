from django.shortcuts import render
import urllib  
import urllib2
import xml.etree.ElementTree as ET
import datetime
import json



#def getUrl():
client_id = "155928392892-mrk26jrg5upa9mpt1ug6d6kest7u2j9b.apps.googleusercontent.com"
client_secret = "yAQ4V4IfLFvy92YypD7hVshI"
scope = "http://gdata.youtube.com https://www.googleapis.com/auth/yt-analytics.readonly"
redirect_uri = "http://localhost:8000/home.html"
tokenUrl = "https://accounts.google.com/o/oauth2/auth?"
state = "profile"
access_type = "offline"
response_type = "code"

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

def register(requst):
    return render(requst,'register.html')

def login(request):
    token = {'scope': scope, 
             'client_id':client_id,
             'response_type': response_type, 
             'redirect_uri':redirect_uri,
             'state':state,
             'access_type': access_type}
    authSubUrl = tokenUrl + urllib.urlencode(token)
    return render(request,'login.html',{
                                        'login_url': authSubUrl,
                                        })
    
def home(request):
    code = request.GET['code']
    newToken = {'code': code, 
                'client_id':client_id,
                'client_secret':client_secret,
                'redirect_uri':redirect_uri,
                'grant_type':'authorization_code'}
    #authurl = tokenUrl + urllib.urlencode(newToken)
    url = "https://accounts.google.com/o/oauth2/token"
    result=post(url, newToken)
    result=json.loads(result)
    access_token=result['access_token']   
    newurl='https://gdata.youtube.com/feeds/api/users/default?'
    token={'v':'2.1', 'access_token':access_token}
    urll = newurl + urllib.urlencode(token)
    #print "hehe " + urll
    result = urllib.urlopen(newurl + urllib.urlencode(token)).read()
    root=ET.fromstring(result) 
    user_id = root.findtext('{http://gdata.youtube.com/schemas/2007}userId')
    user_name = root.find('{http://gdata.youtube.com/schemas/2007}username').attrib['display']
    total_view = root.find('{http://gdata.youtube.com/schemas/2007}statistics').attrib['totalUploadViews']
    view = getLevel(int(total_view))
    num_sub = root.find('{http://gdata.youtube.com/schemas/2007}statistics').attrib['subscriberCount']
    sub = getLevel(int(num_sub))
    image_src = root.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url']
    total_upload = root.findall('{http://schemas.google.com/g/2005}feedLink')[8].attrib['countHint']
    upl = getLevel(int(total_upload))
    now = datetime.datetime.now() 
    now1 = now.strftime("%Y-%m-%d")
    newurl2='https://www.googleapis.com/youtube/analytics/v1/reports?'
    newtoken={'v':'2.1', 
              'end-date': now1,
              'ids':'channel=='+user_id,
              'metrics':'comments,likes',
              'start-date':'2010-10-10',
              'access_token':access_token}
    ll = newurl2+urllib.urlencode(newtoken)
    result2=urllib.urlopen(ll).read()
    result2=json.loads(result2)
    comments, likes = map(int, result2['rows'][0])
    com = getLevel(int(comments));
    lik = getLevel(int(likes))
    return render(request,'home.html',{
                                       'user_name' : user_name,
                                       'image_src' : image_src,
                                       'access_token' : access_token,
                                       'code' : code,
                                       'total_view' : view,
                                       'num_sub' : sub,
                                       'num_upl' : upl,
                                       'num_com' : com,
                                       'num_lik' : lik,
                                       })

def data(request):
    access_token = request.GET['access_token']
    
    newurl='https://gdata.youtube.com/feeds/api/users/default?'
    token={'v':'2.1', 'access_token':access_token}
    urll = newurl + urllib.urlencode(token)
    result = urllib.urlopen(urll).read()
    root=ET.fromstring(result) 
    user_id = root.findtext('{http://gdata.youtube.com/schemas/2007}userId')
    user_name = root.find('{http://gdata.youtube.com/schemas/2007}username').attrib['display']
    last_name=root.find('{http://gdata.youtube.com/schemas/2007}lastName')
    first_name=root.find('{http://gdata.youtube.com/schemas/2007}firstName')
    num_sub = root.find('{http://gdata.youtube.com/schemas/2007}statistics').attrib['subscriberCount']
    now = datetime.datetime.now() 
    now1 = now.strftime("%Y-%m-%d")
    newurl2='https://www.googleapis.com/youtube/analytics/v1/reports?'
    newtoken={'v':'2.1', 
              'end-date': now1,
              'ids':'channel=='+user_id,
              'metrics':'views,comments,likes,dislikes,shares',
              'start-date':'2010-10-10',
              'access_token':access_token}
    ll = newurl2+urllib.urlencode(newtoken)
    result2=urllib.urlopen(ll).read()
    result2=json.loads(result2)
    views, comments, likes, dislikes, shares = map(int, result2['rows'][0])
    vie_lev = numLevel(views)
    sub_lev = numLevel(num_sub)
    com_lev = numLevel(comments)
    lik_lev = numLevel(likes)
    dis_lev = numLevel(dislikes)
    sha_lev = numLevel(shares)
    return render(request,'data.html',{
                                       'user_name' : user_name,
                                       'first_name' : first_name,
                                       'last_name' : last_name,
                                       'num_sub' : num_sub,
                                       'num_view' : views,
                                       'num_com' : comments,
                                       'num_lik' : likes,
                                       'num_dis' : dislikes,
                                       'num_sha' : shares,
                                       'vie_lev' : vie_lev,
                                       'sub_lev' : sub_lev,
                                       'com_lev' : com_lev,
                                       'lik_lev' : lik_lev,
                                       'dis_lev' : dis_lev,
                                       'sha_lev' : sha_lev,
                                       })
    
def getLevel(data):
    base = 271
    if data >= 0 and data<= 100:
        height = (data-0) * base / 100
        return height
    if data > 100 and data <= 1000:
        height = (data-100) * base / 900
        return height
    if data > 1000 and data <= 10000:
        height = (data-1000) * base / 9000
        return height
    if data > 10000 and data <= 50000:
        height = (data-10000) * base / 40000
        return height
    if data > 50000 and data <= 100000:
        height = (data-50000) * base / 50000
        return height
    if data > 100000 and data <= 500000:
        height = (data-100000) * base / 400000
        return height
    if data > 500000 and data <= 1000000:
        height = (data-500000) * base / 500000
        return height
    else:
        return 1

def numLevel(data):
    if data > 0 and data<= 100:
        return 1
    if data > 100 and data <= 1000:
        return 2
    if data > 1000 and data <= 10000:
        return 3
    if data > 10000 and data <= 50000:
        return 4
    if data > 50000 and data <= 100000:
        return 5
    if data > 100000 and data <= 500000:
        return 6
    if data > 500000 and data <= 1000000:
        return 7
    else:
        return 0
