# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache
from models import *
from tvserver.common.jsonconst import *
from tvserver.common import xiaomidata
import datetime
import cjson
import json
import bson
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
@login_required 
def index(request):
    user = request.user
    title = "站点管理"
    root_path = "/cms"
    app_list = []
    model_dict = {}
    model_dict["model_dict"] = "mode_name"
    model_dict["admin_url"] = "admin_url"
    model_dict["perms"] = "perms"
    app = {}
    app["name"] = "name"
    app["app_url"] = "kks"
    app["models"] = [model_dict]
    return render_to_response("admin/index.html", locals())


