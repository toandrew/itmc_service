# -*- coding: utf-8 -*-
import urllib2
import urllib
import hashlib
import gzip
import time
import random
import hmac
from cStringIO import StringIO
import cjson
from jsonconst import *

"""
deviceid = "ef1061bd285568688c7b078f18dee30e"
apiver = "1.8"
ver = "4.3.5"
ptf = "199"
"""
user_data = "&deviceid=ef1061bd285568688c7b078f18dee30e&apiver=1.8&ver=4.3.5&ptf=199&"
#ts = str(int(time.time()))
#nonce = random.randint(-2147483648,2147483647)
key = "581582928c881b42eedce96331bff5d3"

token = "0f9dfa001cba164d7bda671649c50abf"

domain = "http://mobile.duokanbox.com"

def make_signature(path,data,key=key,token=token):
    data = path + "?" + data + "&token=" + token
    signature = hmac.new(key, data, hashlib.sha1).hexdigest()
    return signature

def turn_utf8(data_map):
    for i in data_map:
        if type(data_map[i]) == unicode:
            data_map[i] = data_map[i].encode("utf-8")
    return data_map
    
def get_data(path,data_map):
    url = domain + path
    random_map = {"ts":int(time.time()),"nonce":random.randint(-2147483648,2147483647)}
    data_map = turn_utf8(data_map)
    data = urllib.urlencode(data_map) + user_data + urllib.urlencode(random_map)
    signature = make_signature(path,data)
    data = data + "&opaque=" + signature

    req=urllib2.urlopen(url,data)
    file_content = req.read()
    if req.headers.get('Content-Encoding') == "gzip":
        buf = StringIO(file_content)
        f = gzip.GzipFile(fileobj=buf)
        file_content = f.read()
        f.close()
    return file_content

def get_channel_info(channelid=-1):
    data = {}
    data = {"channelid":channelid}
    json_data = get_data("/tvservice/getchannelinfo",data)
    return cjson.decode(json_data.decode("utf-8"))

def get_banner_media(channelid=0):
    data = {"channelid":channelid}
    json_data = get_data("/tvservice/getbannermedia",data)
    return cjson.decode(json_data.decode("utf-8"))

def get_channel_recommendmedia(channelids=-1,pageno=1,pagesize=3,orderby=-1,listtype=-1,postertype=-1):
    data = {}
    data["channelid"] = channelids
    data["pageno"] = pageno
    data["pagesize"] = pagesize
    data["orderby"] = orderby
    data["listtype"] = listtype
    data["postertype"] = postertype
    json_data = get_data("/tvservice/getchannelrecommendmedia",data)
    return cjson.decode(json_data.decode("utf-8"))

def get_channel_media_list(channelids=50331648,pageno=1,pagesize=15,orderby=2,listtype=-1,postertype=-1,searchtype=-1):
    data = {}
    data["channelids"] = channelids
    data["pageno"] = pageno
    data["pagesize"] = pagesize
    data["orderby"] = orderby
    data["listtype"] = listtype
    data["postertype"] = postertype
    data["searchtype"] = searchtype
    json_data = get_data("/tvservice/filtermediainfo",data)
    return cjson.decode(json_data.decode("utf-8"))

def get_media_detail(mediaid=1018982,fee=1,pageno=1,pagesize=1000,orderby=-1):
    data = {}
    data["mediaid"] = mediaid
    data["fee"] = fee
    data["pageno"] = pageno
    data["pagesize"] = pagesize
    data["orderby"] = orderby
    json_data = get_data("/tvservice/getmediadetail2", data)
    return cjson.decode(json_data.decode("utf-8"))

def get_media_url(mediaid=1021562,ci=1,source=-1):
    data = {}
    data["mediaid"] = mediaid
    data["ci"] = ci
    data["source"] = source
    json_data = get_data("/tvservice/getmediaurl",data)
    return cjson.decode(json_data.decode("utf-8"))

def get_ranking_list_media(channelid=33685509,pageno=1,pagesize=3,postertype=-1,listtype=-1,orderby=-1):
    if int(channelid) in ROOT_CHANNEL:
        data = {}
        data["channelid"] = channelid
        data["pageno"] = pageno
        data["pagesize"] = pagesize
        data["postertype"] = postertype
        data["listtype"] = listtype
        data["orderby"] = orderby
        json_data = get_data("/tvservice/getrankinglistmediainfor",data)
        return cjson.decode(json_data.decode("utf-8"))
    else:
        return get_channel_media_list(channelids=channelid,pageno=pageno,pagesize=pagesize,listtype=listtype,postertype=postertype)

def search_media(medianame="c",pageno=1,pagesize=10,searchtype=1102,searchmask=0):
    data = {}
    data["medianame"] = medianame
    data["pageno"] = pageno
    data["pagesize"] = pagesize
    data["searchtype"] = searchtype
    data["searchmask"] = searchmask
    json_data = get_data("/tvservice/searchmedia",data)
    return cjson.decode(json_data.decode("utf-8"))

if __name__ == "__main__":
    import json
    #data = {"channelid":-1}
    #print get_data('/tvservice/getchannelinfo',data)
    #data = {"channelids":"38,75,52"}
    #print get_data('/tvservice/gettvprogram',data)
    data_str = r"""
{"orderby": "-1", "nonce": "-923312304", "ver": "4.3.5", "pageno": "1", "pagesize": "15", "opaque": "ce42b5ad275e589c8de795c425f78b599ec5c2f4", "ptf": "199", "channelid": "83886080", "ts": "1395047101", "apiver": "1.8", "deviceid": "ef1061bd285568688c7b078f18dee30e", "userbehavdata": "{\"categoryid\":\"\u7eaa\u5f55\u7247(83886080)\",\"time\":1395047101341,\"ime\":\"355136058975049\",\"type\":\"feature\",\"start\":1,\"appVersion\":2014030510,\"ip\":-116873024}", "listtype": "-1", "postertype": "-1"}
    """
    data = json.loads(data_str.strip())
    data.pop("nonce")
    data.pop("ver")
    data.pop("opaque")
    data.pop("ptf")
    data.pop("ts")
    data.pop("apiver")
    data.pop("deviceid")
    data = turn_utf8(data)
    #print get_data('/tvservice/getchannelrecommendmedia',data)
    print get_ranking_list_media()

