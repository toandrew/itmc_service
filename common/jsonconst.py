# -*- coding: utf-8 -*-
#--- request field ---
REQ_SEARCH_TYPE = 1102

#--- response field ---
RES_DATA = "data"
RES_STATUS_CODE = "status"
RES_SEARCH_MEDIA_LIST = "mediainfo"
RES_SEARCH_CHANNEL = "channel"

#--- return code ---
STATUS_SUCCESS = 0
STATUS_ARGUMENT_ERROR = 101


#--- cache heads ---
MEDIA_HEAD = 'm_'
SPIDER_HEAD = 's_m_'
SPIDER_RANK_HEAD = 's_r_'
M3U8_HEAD = 'm3u8_'
SOURCE_URL_HEAD = "source_url_"

#--- cache times ---
MEDIA_CACHE_TIME = 21600 #60*60*6
MEDIA_RANK_LIST_CACHE_TIME = 21600 #60*60*6
M3U8_CACHE_TIME = 7200 #60*60*2
SOURCE_URL_CACHE_TIME = 600 #60*10

#--- meida data  ---
CATEGORY_ID_TO_NAME = {
    "83886080":"纪录片",
    "50331648":"动漫",
    "33554432":"电视剧",
    "67108864":"综艺",
    "16777216":"电影",
    }

CATEGORY_NAME_TO_ID = {
    "纪录片":"83886080",
    "动漫":"50331648",
    "电视剧":"33554432",
    "综艺":"67108864",
    "电影":"16777216",
    }

ROOT_CHANNEL = [83886080,50331648,33554432,67108864,16777216]
