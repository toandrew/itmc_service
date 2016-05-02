# -*- coding: utf-8 -*-
from django.contrib import admin
from tvserver.server.models import *

def make_published(modeladmin, request, queryset):
    queryset.update(is_pub=True)
make_published.short_description = u"批量发布"

class SiteAdmin(admin.ModelAdmin):
    list_display = ("siteid","name")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("channelid","channelname")

class BannerMediaAdminAdmin(admin.ModelAdmin):
    list_display = ("rank","uptime","site","category","mediaid","medianame","img","is_pub")
    list_filter = ("site",)
    actions = [make_published]

class RecommendMediaAdminAdmin(admin.ModelAdmin):
    list_display = ("rank","uptime","site","category","mediaid","medianame","img","is_pub")
    list_filter = ("site",)
    actions = [make_published]

admin.site.register(BannerMediaAdmin,BannerMediaAdminAdmin)
admin.site.register(RecommendMediaAdmin,RecommendMediaAdminAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Site,SiteAdmin)
