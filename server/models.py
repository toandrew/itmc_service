#coding:utf-8
from django.db import models
import mongoengine
from mongoengine import Document
from mongoengine.fields import *

mongoengine.connect("tvserver")

#设备信息
class Device(Document):
    deviceid = StringField(unique = True, max_length = 100)

# 分类信息
class Category(models.Model):
    channelid = models.BigIntegerField(verbose_name=u"id")
    channelname = models.CharField(max_length=200,verbose_name=u"名称")
    class Meta:
        verbose_name = "分类管理"
        verbose_name_plural = "分类管理"
    def __unicode__(self):
        return self.channelname

# 分类信息
class Site(models.Model):
    siteid = models.BigIntegerField(verbose_name=u"id")
    name = models.CharField(max_length=200,verbose_name=u"位置")
    class Meta:
        verbose_name = "位置管理"
        verbose_name_plural = "位置管理"
    def __unicode__(self):
        return self.name

#banner信息
class BannerMedia(Document):
    channelid = IntField(unique = True)
    data =ListField() 

#banner信息admin
class BannerMediaAdmin(models.Model):
    mediaid = models.BigIntegerField(verbose_name=u"mediaid")
    medianame = models.CharField(max_length=200,verbose_name=u"名称")
    site = models.ForeignKey(Site,verbose_name=u"位置")
    category = models.ForeignKey(Category,verbose_name=u"分类")
    rank = models.IntegerField(verbose_name=u"顺序")
    is_pub = models.BooleanField(blank=True,verbose_name=u"是否发布")
    md5 = models.CharField(max_length=64,blank=True,verbose_name=u"图片md5")
    posterurl =  models.CharField(max_length=200,blank=True,verbose_name=u"图片地址") 
    img = models.ImageField(upload_to="itmc/banner/%Y/%m/%d",blank=True, verbose_name="上传图片")
    uptime = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name = "banner管理"
        verbose_name_plural = "banner管理"
        ordering = ["site","category","is_pub","rank","uptime"]

# 推荐页内容
class RecommendMedia(Document):
    channelid = IntField(unique = True)
    data =ListField()

#频道推荐admin
class RecommendMediaAdmin(models.Model):
    mediaid = models.BigIntegerField(verbose_name=u"mediaid")
    medianame = models.CharField(max_length=200,verbose_name=u"名称")
    site = models.ForeignKey(Site,verbose_name=u"位置")
    category = models.ForeignKey(Category,verbose_name=u"分类")
    rank = models.IntegerField(verbose_name=u"顺序")
    is_pub = models.BooleanField(blank=True,verbose_name=u"是否发布")
    md5 = models.CharField(max_length=64,blank=True,verbose_name=u"图片md5")
    posterurl =  models.CharField(max_length=200,blank=True,verbose_name=u"图片地址") 
    img = models.ImageField(upload_to="itmc/recommend/%Y/%m/%d",blank=True, verbose_name="上传图片")
    uptime = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name = "频道推荐管理"
        verbose_name_plural = "频道推荐管理"
        ordering = ["site","category","is_pub","rank"]

#频道信息
class ChannelInfo(Document):
    channel = ListField()

# 媒体详情
class MediaDetailInfo(Document):
    mediaid = IntField(unique = True)
    medianame = StringField(max_length = 348)
    actors = StringField(max_length = 768)
    area = StringField(max_length = 48)
    category = StringField(max_length = 96)
    allcategorys = StringField(max_length = 96)
    director = StringField(max_length = 96)
    issuedate = DateTimeField()
    lastissuedate = DateTimeField()
    posterurl = StringField(max_length = 300)
    md5 = StringField(max_length = 64)
    midtype = IntField()
    playcount = IntField()
    playlength = IntField() 
    resolution = IntField() 
    score = IntField() 
    scorecount = IntField() 
    ismultset = IntField()
    setcount = IntField()
    setnow = IntField()
    flag = IntField()
    desc = StringField()
    mediaciinfo = DictField()
    meta = {
        'indexes': ['medianame']
            }

# 视频地址
class MediaUrl(Document):
    mediaid = IntField()
    ci = IntField()
    videoname = StringField(max_length = 348)
    normal = ListField()
    high = ListField()
    super = ListField()
    meta = {
        'indexes': [('mediaid', 'ci')]
            }

# 标签 
class Tag(Document):
    name = StringField(max_length = 48,unique = True)
    property = models.IntegerField()
    
# 地区
class Area(Document):
    name = StringField(max_length = 48,unique = True)

# 播放历史
class History(Document):
    deviceid = StringField(max_length = 100)
    mediaid = IntField()
    ci = IntField()
    url = StringField(max_length = 300)
    playtime = IntField()
    updatetime= DateTimeField()

# 收藏
class Bookmark(Document):
    deviceid = StringField(max_length = 100)
    mediaid = IntField()
    updatetime= DateTimeField()
