# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache
from models import *
from tvserver.common.jsonconst import *
from tvserver.common import xiaomidata
from tvserver.common import parserealurl
import datetime
import cjson
import json
import bson


def login(request):
    id = request.GET.get("deviceid","")
    if not id:
        return HttpResponse("id is null")
    device = Device.objects.get(deviceid=id)
    if device:
        device = Device(deviceid=id)
        device.save()
    else:
        pass
    return HttpResponse("ok")

def getm3u8url(mediaid,ci,source):
    url = "http://demo.bibifa.com/m3u8/%s/%s/%s/m3u8.m3u8" %(mediaid,ci,source)
    return url

def getm3u8(request,mediaid,ci,source):
    content = cache.get(M3U8_HEAD+"_"+mediaid+"_"+ci+"_"+source)
    if not content:
        content = ""
    return HttpResponse(content)

def setm3u8(mediaid,ci,source,url_list):
    m3u_list = ["#EXTM3U"]
    m3u_list.extend(url_list)
    content = "\n".join(m3u_list)
    cache.set(M3U8_HEAD+"_"+mediaid+"_"+ci+"_"+source,content,M3U8_CACHE_TIME)

def getchannellist(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    channel_info_list= ChannelInfo.objects.all()
    channel_info = channel_info_list[0]
    res_json[RES_DATA] = channel_info.channel
    return HttpResponse(cjson.encode(res_json))

def getbannermedia(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    channelid = request.GET.get("channelid","0")
    banner_media = BannerMedia.objects.get(channelid=channelid)
    res_json[RES_DATA] = banner_media.data
    return HttpResponse(cjson.encode(res_json))

def getchannelrecommendmedia(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    channelid = request.GET.get("channelid","-1")
    channel_recommend_media = RecommendMedia.objects.get(channelid=channelid)
    res_json[RES_DATA] = channel_recommend_media.data
    return HttpResponse(cjson.encode(res_json))

def getmedialist(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    channelid = request.GET.get("channelid","0")
    pageno = int(request.GET.get("pageno","1"))
    pagesize = int(request.GET.get("pagesize","100"))
    orderby = request.GET.get("orderby","1")
    if orderby:
        if int(channelid) in ROOT_CHANNEL:
            if orderby == "1":
                    media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("-issuedate")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "2":
                media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("issuedate")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "3":
                media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("-score")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "4":
                media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("score")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "5":
                media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("-playcount")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "6":
                media_list = MediaDetailInfo.objects.filter(category=CATEGORY_ID_TO_NAME[channelid]).order_by("playcount")[(pageno-1)*pagesize:pageno*pagesize]
            elif orderby == "7":
                temp_data = cache.get(SPIDER_RANK_HEAD+"_"+str(channelid)+"_"+str(pageno)+"_"+str(pagesize))
                if temp_data:
                    temp_data = get_field_data_form_json(temp_data.encode("utf-8")) 
                else:
                    temp_data = xiaomidata.get_ranking_list_media(channelid=channelid,pageno=pageno,pagesize=pagesize)["data"]
                    cache.set(SPIDER_RANK_HEAD+"_"+str(channelid)+"_"+str(pageno)+"_"+str(pagesize),cjson.encode(temp_data),MEDIA_RANK_LIST_CACHE_TIME)
                res_json[RES_DATA] = temp_data 
        else:
            # get xiaomi data
            #todo cache
            temp_data = cache.get(SPIDER_RANK_HEAD+"_"+str(channelid)+"_"+str(pageno)+"_"+str(pagesize))
            if temp_data:
                temp_data = get_field_data_form_json(temp_data.encode("utf-8")) 
            else:
                temp_data = xiaomidata.get_ranking_list_media(channelid=channelid,pageno=pageno,pagesize=pagesize)["data"]
                cache.set(SPIDER_RANK_HEAD+"_"+str(channelid)+"_"+str(pageno)+"_"+str(pagesize),cjson.encode(temp_data),MEDIA_RANK_LIST_CACHE_TIME)
            res_json[RES_DATA] = temp_data 
        if orderby != "7" and int(channelid) in ROOT_CHANNEL:
            media_map_list = []
            for i in media_list:
                media_map_list.append(get_field_data_form_obj(i))
            res_json[RES_DATA] = media_map_list
    else:
        res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def getmediadetail(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    mediaid = request.GET.get("mediaid","")
    if mediaid:
        data = get_media(mediaid)
        res_json[RES_DATA] = data
    else:
        res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def getmediaurl(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    mediaid = request.GET.get("mediaid","")
    ci = request.GET.get("ci","")
    source = request.GET.get("source","")
    sort = int(request.GET.get("sort","0"))
    is_list = request.GET.get("islist","")
    if is_list == "true":
        islist = True
    else:
        islist = False
    content = cache.get(SOURCE_URL_HEAD+"_"+mediaid+"_"+ci+"_"+source+"_"+str(sort)+"_"+str(islist))
    if content:
        res_json["url"] = content
        return HttpResponse(cjson.encode(res_json))
    if mediaid and ci:
        media_url_list = MediaUrl.objects.filter(mediaid=mediaid,ci=ci)
        #todo add cache
        if len(media_url_list) > 0:
            media_url = media_url_list[0]
        else:
            temp_url = xiaomidata.get_media_url(mediaid=mediaid,ci=ci)
            media_url = MediaUrl(
                mediaid=mediaid,
                ci=ci,
                videoname=temp_url["videoname"],
                normal=temp_url["normal"],
                high = temp_url["high"],
                super = temp_url["super"],
                )
            media_url.save()
        temp_data = {}
        temp_data["videoname"] = media_url.videoname
        temp_data["normal"] = media_url.normal
        temp_data["high"] = media_url.high
        temp_data["super"] = media_url.super
        if source:
            source_url = ""
            for i in ["high","normal","super"]:
                for j in temp_data[i]:
                    if str(j["source"]) == source:
                        source_url = j["playurl"].replace("\\","")
                        break 
            if source_url:
                url = parserealurl.parse_url(source,source_url,sort,islist)
                if url:
                    cache.set(SOURCE_URL_HEAD+"_"+mediaid+"_"+ci+"_"+source+"_"+str(sort)+"_"+str(islist),url,SOURCE_URL_CACHE_TIME)
                res_json["url"] = url
        else: 
            res_json[RES_DATA] = temp_data
    else:
       res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def setplayhistory(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    mediaid = request.GET.get("mediaid","")
    ci = int(request.GET.get("ci","0"))
    url = request.GET.get("url","")
    playtime = int(request.GET.get("playtime","0"))
    if deviceid and mediaid and ci and url and playtime:
        history_list = History.objects.filter(deviceid=deviceid, mediaid=mediaid)
        if len(history_list) > 0:
            history = history_list[0]
            history.ci = ci
            history.url = url
            history.playtime = playtime
            history.updatetime = datetime.datetime.now()
        else:
            history = History(deviceid=deviceid, mediaid=mediaid, ci=ci, url=url, playtime=playtime, updatetime=datetime.datetime.now())
        history.save()
    else:
        res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def getplayhistory(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    if deviceid:
        bookmark_list = Bookmark.objects.filter(deviceid=deviceid).only("mediaid")
        bookmark_set = set()
        for i in bookmark_list:
            bookmark_set.add(i.mediaid)
        history_list = History.objects.filter(deviceid=deviceid).order_by("updatetime")
        temp_data = []
        mediaid_list = []
        for i in history_list:
            data = get_field_data_form_obj(i)
            mediaid_list.append(i.mediaid)
            temp_data.append(data)
        media_list = get_media(mediaid_list)
        temp_data = map_merge(history_list,media_list,'mediaid')
        res_json[RES_DATA] = temp_data
        return HttpResponse(cjson.encode(res_json))
    res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def deleteplayhistory(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    if deviceid:
        History.objects.filter(deviceid=deviceid).delete()
        return HttpResponse(cjson.encode(res_json))
    res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def setbookmark(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    mediaid = request.GET.get("mediaid","")
    if deviceid and mediaid:
        bookmark_list = Bookmark.objects.filter(deviceid=deviceid, mediaid=mediaid).order_by("updatetime")
        if len(bookmark_list) > 0:
            bookmark = bookmark_list[0]
            bookmark.updatetime = datetime.datetime.now()
        else:
            bookmark = Bookmark(deviceid=deviceid, mediaid=mediaid, updatetime=datetime.datetime.now())
        bookmark.save()
        return HttpResponse(cjson.encode(res_json))
    res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def getbookmark(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    if deviceid:
        bookmark_list = Bookmark.objects.filter(deviceid=deviceid).order_by("-updateTime")
        media_list = []
        bookmark_map_list = []
        for i in bookmark_list:
            media_list.append(i.mediaid)
            bookmark_map_list.append(get_field_data_form_obj(i))
        media_obj_list = get_media(media_list) 
        temp_data = map_merge(bookmark_map_list,media_obj_list,"mediaid") 
        res_json[RES_DATA] = temp_data
        return HttpResponse(cjson.encode(res_json))
    res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def deletebookmark(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    deviceid = request.GET.get("deviceid","")
    mediaid = request.GET.get("mediaid","")
    if deviceid and mediaid:
        Bookmark.objects.filter(deviceid=deviceid,mediaid=mediaid).delete()
        return HttpResponse(cjson.encode(res_json)) 
    res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def searchmedia(request):
    res_json = {}
    res_json[RES_STATUS_CODE] = STATUS_SUCCESS
    data = {}
    pageno = int(request.GET.get("pageno","1"))
    pagesize = int(request.GET.get("pagesize","10"))
    orderby = request.GET.get("orderby","0")
    s_type = int(request.GET.get("type","0"))
    keyword = request.GET.get("keyword","")
    if s_type == REQ_SEARCH_TYPE:
        res_json[RES_DATA] = xiaomidata.search_media(medianame=keyword,pageno=pageno,pagesize=pagesize)["data"]
    elif keyword:
        media_list = MediaDetailInfo.objects.filter(medianame__contains=keyword)[(pageno-1)*pagesize:pageno*pagesize]
        media_map_list = []
        channle_count_map = {}
        for i in media_list:
            media_map_list.append(get_field_data_form_obj(i))
            if channle_count_map.has_key(i.category):
                channle_count_map[i.category] = channle_count_map[i.category] + 1
            else:
                channle_count_map[i.category] = 1
        channle_map_list = []
        for i in channle_count_map:
            temp_map = {}
            temp_map["name"] = i
            temp_map["count"] = channle_count_map[i]
            temp_map["channelid"] = int(CATEGORY_NAME_TO_ID[i.encode("utf-8")])
            channle_map_list.append(temp_map)
        data[RES_SEARCH_CHANNEL] = channle_map_list
        data[RES_SEARCH_MEDIA_LIST] = media_map_list
        res_json[RES_DATA] = data
    else:
        res_json[RES_STATUS_CODE] = STATUS_ARGUMENT_ERROR
    return HttpResponse(cjson.encode(res_json))

def get_media(mediaid,field_list = []):
    if type(mediaid) == list:
        return_list = []
        no_cache_list = []
        temp_map = {}
        for i in mediaid:
            media = cache.get(MEDIA_HEAD+str(i).strip())
            if media:
                temp_map[str(i).strip()] = get_field_data_form_json(media,field_list)
            else:
                no_cache_list.append(str(i).strip())
        media_list = MediaDetailInfo.objects.filter(mediaid__in=no_cache_list)
        for i in media_list:
            temp_map[i.mediaid] = get_field_data_form_obj(i)
            cache.set(MEDIA_HEAD+str(i.mediaid),cjson.encode(get_field_data_form_obj(i)),MEDIA_CACHE_TIME)
        for i in mediaid:
            if temp_map.has_key(str(i).strip()):
                return_list.append(temp_map[str(i).strip()])
        return return_list
    else:
        media = cache.get(MEDIA_HEAD+str(mediaid))
        if media:
            return get_field_data_form_json(media,field_list)
        else:
            media_obj = MediaDetailInfo.objects.filter(mediaid=mediaid)
            if len(media_obj) > 0:
                cache.set(MEDIA_HEAD+str(mediaid),cjson.encode(get_field_data_form_obj(media_obj[0])),MEDIA_CACHE_TIME)
                return get_field_data_form_obj(media_obj[0],field_list)
            else:
                media_obj = get_detail_from_spider(mediaid)
                return get_field_data_form_obj(media_obj,field_list)

def get_field_data_form_json(json_data,field_list=[]):
    if len(field_list) == 0:
        return cjson.decode(json_data)
    else:
        try:
            data = cjson.decode(json_data)
        except:
            data = {}
        temp_data = {}
        for i in data:
            if i in field_list:
                temp_data[i] = data[i]
        return temp_data

def get_field_data_form_obj(obj,field_list=[]):
    if len(field_list) == 0:
        #kk = dir(obj)
        field_list = obj._fields.keys()
    temp_data = {}
    #type_list = []
    for i in field_list:
        temp_data[i] = getattr(obj,i,"")
        if type(temp_data[i]) == datetime.datetime:
            temp_data[i] = temp_data[i].strftime("%y-%m-%d %H:%M:%S")
        elif type(temp_data[i]) == bson.objectid.ObjectId:
            temp_data[i] = str(temp_data[i])
        #type_list.append(type(temp_data[i]))
    return temp_data

def map_merge(master_list,cluster_list,key):
    temp_list = []
    if type(key) == list:
        for i in master_list:
            for j in cluster_list:
                if key_equal(i,j,key):
                    i.update(j)
                    break
            temp_list.append(i)
    else:
        for i in master_list:
            if i.has_key(key):
                for j in cluster_list:
                    if j.has_key(key):
                        if i[key] == j[key]:
                            i.update(j)
                            break
            temp_list.append(i)
    return temp_list

def key_equal(map_a,map_b,key):
    for i in key:
        if map_a.has_key(i) and map_b.has_key(i):
            if map_a[i] == map_b[i]:
                pass
            else:
                return False
        else:
            return False
    return True

def map_change_key(map_list,old_key,new_key):
    temp_list = []
    for i in map_list:
        if i.has_key(old_key):
            value = i.pop(old_key)
            i[new_key] = value
            temp_list.append[i]
    return temp_list

def get_detail_from_spider(mediaid):
    media_detail_list = MediaDetailInfo.objects.filter(mediaid=mediaid)
    if len(media_detail_list) > 0:
        media_detail = mdeia_detail_list[0]
    else:
        mediaid_data = xiaomidata.get_media_detail(mediaid)
        mediaciinfo = mediaid_data["data"]["mediaciinfo"]
        mediainfo = mediaid_data["data"]["mediainfo"]
        mediainfo["mediaciinfo"] = mediaciinfo
        if mediainfo["issuedate"]:
            issuedate = datetime.datetime.strptime(mediainfo["issuedate"], "%Y-%m-%d")
        else:
            issuedate = None
        if mediainfo["lastissuedate"]:
            lastissuedate = datetime.datetime.strptime(mediainfo["lastissuedate"], "%Y-%m-%d")
        else:
            lastissuedate = None
        media_detail = MediaDetailInfo(
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
        media_detail.save()
    return media_detail

