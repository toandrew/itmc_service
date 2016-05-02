# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import base64
import json
from urlparse import urlparse

re_url_area = re.compile("下载地址(.*?)</td>", re.S)
re_url_list = re.compile('<a href="(.*?)"', re.S)

def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote, s.split('='))
            d[k] = v
    return d

def parse_url_flvcd(url):
    post_url = "http://www.flvcd.com/parse.php"
    data = {}
    data["kw"] = url
    data["format"] = "super"
    content = urllib2.urlopen(post_url+"?"+urllib.urlencode(data)).read()
    content = content.decode("GBK").encode("utf8")
    url_areas = re_url_area.findall(content)
    if len(url_areas) > 0:
        url_area = url_areas[0]
    else:
        url_area = ""
    url_list = re_url_list.findall(url_area)
    if len(url_list) > 0:
        return url_list[0]
    else:
        return ""

def select_m3u8(m3u8_list):
    for i in m3u8_list:
        if i.find(u"超清") >= 0:
            return i
    for i in m3u8_list:
        if i.find(u"高清") >= 0:
            return i
    for i in m3u8_list:
        if i.upper().find("MP4") >= 0:
            return i
    return m3u8_list[0]

def select_quality(quality_list,selcet_list=[]):
    for i in quality_list:
        if i.upper().find(u"1080P") >= 0:
            if len(selcet_list) > 0:
                if i in selcet_list:
                    return i
            else:
                return i
    for i in quality_list:
        if i.find(u"超清") >= 0:
            if len(selcet_list) > 0:
                if i in selcet_list:
                    return i
            else:
                return i
    for i in quality_list:
        if i.find(u"高清") >= 0:
            if len(selcet_list) > 0:
                if i in selcet_list:
                    return i
            else:
                return i
    for i in quality_list:
        if i.upper().find("MP4") >= 0:
            if len(selcet_list) > 0:
                if i in selcet_list:
                    return i
            else:
                return i
    return quality_list[0]

def sort_0(js_content, islist=False):
    url_list = []
    m3u8_list = []
    quality_list = []
    for i in js_content:
        if i.has_key("quality"):
            quality_list.append(i["quality"])
            if i["quality"].encode("utf-8").upper().find("M3U8") >= 0:
                m3u8_list.append(i["quality"])
    if len(m3u8_list) > 0:
        m3u8 = select_m3u8(m3u8_list)
        for i in js_content:
            if i.has_key("quality"):
                if i["quality"] == m3u8:
                    m3u8_content = urllib2.urlopen(i["files"][0]["furl"]).read()
                    #print m3u8_content
                    if m3u8_content.find("BANDWIDTH") >= 0:
                        import logging
                        logger = logging.getLogger("/data/wwwroot/tvserver/log/err.log")
                        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
                        fh = logging.FileHandler("/data/wwwroot/tvserver/log/err.log") 
                        fh.setFormatter(formatter)
                        logger.addHandler(fh)
                        logger.error(i["files"][0]["furl"])
                    return i["files"][0]["furl"]
    else:
        if len(quality_list) > 0:
            quality = select_quality(quality_list)
            for i in js_content:
                if i.has_key("quality"):
                    if i["quality"] == quality:
                        if islist:
                            temp_url_list = []
                            for j in i["files"]:
                                temp_url_list.append(j["furl"])
                            return "||".join(temp_url_list)
                        else:
                            return i["files"][0]["furl"]
    return ""

def sort_1(js_content, islist=False):
    url_list = []
    mp4_list = []
    quality_list = []
    for i in js_content:
        if i.has_key("quality"):
            quality_list.append(i["quality"])
            if len(i["files"]) > 0:
                if i["files"][0].has_key("ftype"):
                    if i["files"][0]["ftype"] == "mp4":
                        mp4_list.append(i["quality"])
    if len(mp4_list) > 0:
        quality = select_quality(quality_list,selcet_list = mp4_list)
        for i in js_content:
            if i.has_key("quality"):
                if i["quality"] == quality:
                    if islist:
                        temp_url_list = []
                        for j in i["files"]:
                            temp_url_list.append(j["furl"])
                        return "||".join(temp_url_list)
                    else:
                        return i["files"][0]["furl"]
    return ""
 
def sort_2(js_content, islist=False):
    url_list = []
    flv_list = []
    quality_list = []
    for i in js_content:
        if i.has_key("quality"):
            quality_list.append(i["quality"])
            if len(i["files"]) > 0:
                if i["files"][0].has_key("ftype"):
                    if i["files"][0]["ftype"] == "flv":
                        flv_list.append(i["quality"])
    if len(flv_list) > 0:
        quality = select_quality(quality_list,selcet_list = flv_list)
        for i in js_content:
            if i.has_key("quality"):
                if i["quality"] == quality:
                    if islist:
                        temp_url_list = []
                        for j in i["files"]:
                            temp_url_list.append(j["furl"])
                        return "||".join(temp_url_list)
                    else:
                        return i["files"][0]["furl"]
    return ""

def sort_3(js_content, islist=False):
    url_list = []
    m3u8_list = []
    quality_list = []
    for i in js_content:
        if i.has_key("quality"):
            quality_list.append(i["quality"])
            if i["quality"].encode("utf-8").upper().find("M3U8") >= 0:
                m3u8_list.append(i["quality"])
    if len(m3u8_list) > 0:
        m3u8 = select_m3u8(m3u8_list)
        for i in js_content:
            if i.has_key("quality"):
                if i["quality"] == m3u8:
                    m3u8_content = urllib2.urlopen(i["files"][0]["furl"]).read()
                    #print m3u8_content
                    if m3u8_content.find("BANDWIDTH") >= 0:
                        import logging
                        logger = logging.getLogger("/data/wwwroot/tvserver/log/err.log")
                        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
                        fh = logging.FileHandler("/data/wwwroot/tvserver/log/err.log") 
                        fh.setFormatter(formatter)
                        logger.addHandler(fh)
                        logger.error(i["files"][0]["furl"])
                    if islist:
                        temp_url_list = []
                        for j in i["files"]:
                            temp_url_list.append(j["furl"])
                        return "||".join(temp_url_list)
                    else:
                        return i["files"][0]["furl"]
      
def parse_url_flvxz(url="",site="",vid="", sort=0, islist=False):
    if url:
        post_url = "http://api.flvxz.com/url/"+base64.b64encode(url.replace("://",":##"))+"/jsonp/purejson"
    else:
        post_url = "http://api.flvxz.com/site/%s/vid/%s/jsonp/purejson" %(site,vid)
    content = urllib2.urlopen(post_url).read()
    #print post_url
    print content
    js_content = json.loads(content)
    #print js_content
    #print sort
    if sort == 0:
        return sort_0(js_content,islist)
    elif sort == 1:
        return sort_1(js_content,islist)
    elif sort == 2:
        return sort_2(js_content,islist)
    elif sort == 3:
        return sort_3(js_content,islist)
    else:
        return sort_0(js_content,islist)

def parse_url(source,url,sort=0,islist=False):
    #return "http://v.youku.com/player/getRealM3U8/vid/XNDUwNjc4MzA4/type/video.m3u8"
    if source == "34":
        get_dic = urldecode(urlparse(url.replace("\\","")).query)
        mediaid = get_dic["mediaid"]
        url = "http://www.funshion.com/vplay/m-%s/" %mediaid
        return parse_url_flvcd(url)
    elif source == "10":
        get_dic = urldecode(urlparse(url.replace("\\","")).query)
        mediaid = get_dic["cid"]
        url = "http://v.qq.com/cover/%s/%s.html" %(mediaid[0],mediaid)
        return parse_url_flvxz(url,sort=sort,islist=islist)
    elif source == "32":
        mediaid = urlparse(url.replace("\\","")).path.replace("/vplay_","").replace(".html","")
        url = "http://www.letv.com/ptv/vplay/%s.html" %mediaid
        return parse_url_flvxz(url,sort=sort,islist=islist)
    elif source == "3":
        url = url.replace("m.tv.sohu.com","tv.sohu.com")
        return parse_url_flvxz(url.replace("\\",""),sort=sort,islist=islist)
        
    return parse_url_flvxz(url=url.replace("\\",""),sort=sort,islist=islist)

if __name__ == "__main__":
    url = "http://3g.v.qq.com/android/player.html?type=1&cid=9q8a0ll3ibmduvz&vid=u0012qr5vr1&protype=10&version=xiaomi1.0.0&hidemp4=1"
    #url = "http://m.funshion.com/subject?mediaid=112875&number=20140213&malliance=1660"
    #url = "http://m.letv.com/vplay_1934457.html?ref=xiaomi"
    #url = "http://m.tv.sohu.com/20140131/n394431306.shtml?src=10000001"
    url = "http://tv.sohu.com/20140520/n399817359.shtml"
    #url = "http://m.iqiyi.com/play.html?tvid=430013&vid=bf2e094d29a346ee9af2d7feb24214dc&msrc=3_69_145"
    #url = "http://www.iqiyi.com/dianying/20130321/1ddfeb732c56810c.html?msrc=3_69_145"
    #url = "http://v.youku.com/v_show/id_XNjk4ODgwMDQw.html"
    #url = "http:\\/\\/www.tudou.com\\/albumplay\\/HyU7HdeWd_w\\/M7xD0Vv1JGo.html?tpa=dW5pb25faWQ9MTAzNDcyXzEwMDAwMV8wMV8wMQ"
    #url = "http:\\/\\/3g.v.qq.com\\/android\\/player.html?type=2&cid=anlxed56zwbpm16&vid=s0014qqdkhn&protype=10&version=xiaomi1.0.0&hidemp4=1"
    #url = "http:\\/\\/m.tv.sohu.com\\/20140319\\/n396889747.shtml?src=10000001"
    #url = "http:\\/\\/3g.v.qq.com\\/android\\/player.html?type=2&cid=bnxrqesmmhl3f3f&vid=d0014e90how&protype=10&version=xiaomi1.0.0&hidemp4=1"
    #url = "http:\\/\\/m.iqiyi.com\\/v_19rrh55uok.html?msrc=3_69_145"
    url = "http:\\/\\/m.iqiyi.com\\/play.html?tvid=223482800&vid=dad4748c6e97f7b04f7c9b3dbba4a9df&msrc=3_69_145"
    #print parse_url("qq",url, 0)
    #url = "http://v.youku.com/v_show/id_XNzI2OTE4NTg4.html"
    print parse_url("sohu",url, 2, islist=True)
    #url = "http://v.pps.tv/play_35EKJB.html"
    #url = "http://tv.sohu.com/20140131/n394431306.shtml?src=10000001"
    #print parse_url_flvxz(url)

