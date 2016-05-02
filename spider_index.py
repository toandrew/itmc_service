import settings
import sys
from django.core.management import setup_environ
sys.path.append(settings.settings_path)
setup_environ(settings)
from django.core.cache import cache
import cjson
import json
from datetime import datetime
from server.models import *
from common.jsonconst import *

from common import xiaomidata

#print cjson.encode(xiaomidata.get_channel_info())
#print cjson.encode(xiaomidata.get_channel_media_list())
#print cjson.encode(xiaomidata.get_media_detail())
#print cjson.encode(xiaomidata.get_media_url(mediaid=1033075,ci=1))
#print cjson.encode(xiaomidata.get_channel_recommendmedia(channelids=50331648,pagesize=15))
#print cjson.encode(xiaomidata.get_banner_media(channelid=0))
#print cjson.encode(xiaomidata.get_ranking_list_media())
#print cjson.encode(xiaomidata.search_media())
media_set = set()
url_set = set()

all_channel = [83886080,50331648,33554432,67108864,16777216]
def init_media():
    for i in all_channel:
        get_channel_media(i)

def get_media_set():
    media_detail_list = MediaDetailInfo.objects.all()
    for i in media_detail_list:
        media_set.add(i.mediaid)

def get_channel_media(channelids):
    #get_media_set()
    temp_data = xiaomidata.get_channel_media_list(channelids)
    count = temp_data["count"]
    max_pageno = count/15+1
    for i in range(1,max_pageno):
        temp_media_list = xiaomidata.get_channel_media_list(channelids,pageno=i)
        media_ids = []
        for j in temp_media_list["data"]:
            print j["mediaid"]
            """
            if j["mediaid"] in media_set:
                continue
            else:
                media_set.add(j["mediaid"])
            """
            save_media(j["mediaid"])

def save_media(mediaid):
    mediaid_data = xiaomidata.get_media_detail(mediaid)
    mediaciinfo = mediaid_data["data"]["mediaciinfo"]
    mediainfo = mediaid_data["data"]["mediainfo"]
    mediainfo["mediaciinfo"] = mediaciinfo
    #print mediainfo
    print mediainfo["mediaid"]
    if mediainfo["issuedate"]:
        issuedate = datetime.strptime(mediainfo["issuedate"], "%Y-%m-%d")
    else:
        issuedate = None
    if mediainfo["lastissuedate"]:
        lastissuedate =  datetime.strptime(mediainfo["lastissuedate"], "%Y-%m-%d")
    else:
        lastissuedate = None
    m_d_i_list = MediaDetailInfo.objects.filter(mediaid=mediainfo["mediaid"])
    if len(m_d_i_list) > 0:
        mdeia_detail = m_d_i_list[0]
        mdeia_detail.medianame = mediainfo["medianame"]
        mdeia_detail.setnow = mediainfo["setnow"]
        mdeia_detail.playcount = mediainfo["playlength"]
        mdeia_detail.lastissuedate = lastissuedate
        mdeia_detail.setcount =  mediainfo["setcount"]
        mdeia_detail.mediaciinfo = mediainfo["mediaciinfo"]
    else:
        mdeia_detail = MediaDetailInfo(
            mediaid = mediainfo["mediaid"],
            medianame = mediainfo["medianame"],
            actors = mediainfo["actors"],
            area = mediainfo["area"],
            category = mediainfo["category"],
            allcategorys = mediainfo["allcategorys"],
            director = mediainfo["director"],
            issuedate = issuedate, 
            lastissuedate = lastissuedate,
            posterurl = mediainfo["posterurl"],
            md5 = mediainfo["md5"],
            midtype = mediainfo["midtype"],
            playcount = mediainfo["playcount"],
            playlength = mediainfo["playlength"],
            resolution = mediainfo["resolution"],
            score = mediainfo["score"],
            scorecount = mediainfo["scorecount"],
            ismultset = mediainfo["ismultset"],
            setcount = mediainfo["setcount"],
            setnow = mediainfo["setnow"],
            flag = mediainfo["flag"],
            desc = mediainfo["desc"],
            mediaciinfo = mediainfo["mediaciinfo"],
            )
    mdeia_detail.save()

def get_url_set():
    media_url = MediaUrl.objects.all()
    for i in media_url:
        url_set.add(str(i.mediaid)+"|"+str(i.ci))

def update_media_url():
    get_url_set()
    count = MediaDetailInfo.objects.count()
    step = 10
    for n in range(0,count+step,step):
        m_d_i = MediaDetailInfo.objects[n*step:(n+1)*step]
        for i in m_d_i:
            setnow = i.setnow
            for j in range(1,setnow+1):
                if str(i.mediaid)+"|"+str(j) in url_set:
                    continue
                else:
                    url_set.add(str(i.mediaid)+"|"+str(j))
                temp_url = xiaomidata.get_media_url(mediaid=i.mediaid,ci=j)
                media_url = MediaUrl(
                    mediaid=i.mediaid,
                    ci=j,
                    videoname=temp_url["videoname"],
                    normal=temp_url["normal"],
                    high = temp_url["high"],
                    super = temp_url["super"],
                    )
                media_url.save()

def update_channel():
    print ChannelInfo.objects.all().delete()
    channel_info = xiaomidata.get_channel_info()["data"]
    c_i = ChannelInfo(channel=channel_info)
    #print channel_info
    c_i.save()

def update_banner():
    print BannerMedia.objects.all().delete()
    all_channel.append(0)
    for i in all_channel:
        banner_media = xiaomidata.get_banner_media(channelid=i)
        banner_media_obj = BannerMedia(channelid=i,data=banner_media["data"])
        banner_media_obj.save()

# for cms
def update_banner_admin():
    all_channel.append(0)
    for i in all_channel:
        banner_media = xiaomidata.get_banner_media(channelid=i)
        site = Site.objects.get(siteid=i)
        for j in banner_media["data"]:
            b_m_a_list = BannerMediaAdmin.objects.filter(site=site,mediaid=j["mediaid"])
            if len(b_m_a_list) == 0:
                if j.has_key("category"):
                    category = Category.objects.get(channelname=j["category"])
                else:
                    category = Category.objects.get(channelid=-1)
                b_a = BannerMediaAdmin(mediaid=j["mediaid"],
                                medianame=j["medianame"],
                                site=site,
                                category = category,
                                rank = j["rank"],
                                md5 = j["md5"],
                                posterurl = j["posterurl"].replace("\\","")
                                )
                b_a.save()

def update_channel_recommend_media():
    print RecommendMedia.objects.all().delete()
    all_channel.append(-1)
    for i in all_channel:
        if i == -1 :
            pagesize = 3
        else:
            pagesize = 15
        channel_recommendmedia = xiaomidata.get_channel_recommendmedia(channelids=i,pagesize=pagesize)
        if i == -1 :
            temp_list = []
            for j in channel_recommendmedia["data"]:
                if j.has_key("midtype"):
                    if j["midtype"] != 600:
                        temp_list.append(j)
            channel_recommendmedia_obj = RecommendMedia(channelid=i,data=temp_list)
        else: 
            channel_recommendmedia_obj = RecommendMedia(channelid=i,data=channel_recommendmedia["data"])
        channel_recommendmedia_obj.save()

# for cms
def update_channel_recommend_media_admin():
    all_channel.append(-1)
    for i in all_channel:
        if i == -1 :
            pagesize = 3
            site = Site.objects.get(siteid=0)
        else:
            pagesize = 15
            site = Site.objects.get(siteid=i)
        channel_recommendmedia = xiaomidata.get_channel_recommendmedia(channelids=i,pagesize=pagesize)
        for j in channel_recommendmedia["data"]:
            if j["id"] not in all_channel:
                continue
            if j["id"] == 0:
                continue
            category = Category.objects.get(channelid=j["id"])
            rank = 0
            for k in j["data"]:
                r_m_a_list = RecommendMediaAdmin.objects.filter(site=site,mediaid=k["mediaid"])
                rank += 1
                if len(r_m_a_list) == 0:
                    r_a = RecommendMediaAdmin(mediaid=k["mediaid"],
                                    medianame=k["medianame"],
                                    site=site,
                                    category = category,
                                    rank = rank,
                                    md5 = k["md5"],
                                    posterurl = k["posterurl"].replace("\\","")
                                    )
                    r_a.save()

            
        #channel_recommendmedia_obj = RecommendMedia(channelid=i,data=channel_recommendmedia["data"])
        #channel_recommendmedia_obj.save()

def get_media_source_set():
    media_detail_list = MediaUrl.objects.all()
    source_map = {}
    for i in media_detail_list:
        for j in i.normal:
            if source_map.has_key(j["source"]):
                continue
            else:
                source_map[j["source"]] = j["playurl"]
        for j in i.high:
            if source_map.has_key(j["source"]):
                continue
            else:
                source_map[j["source"]] = j["playurl"]
        for j in i.super:
            if source_map.has_key(j["source"]):
                continue
            else:
                source_map[j["source"]] = j["playurl"]
          
    for i in source_map:
        print i,source_map[i]

#get_media_source_set()        
#init_media()
#update_media_url()
update_channel()
update_banner()
update_channel_recommend_media()
#update_banner_admin()
#update_channel_recommend_media_admin()
