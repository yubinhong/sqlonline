# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from web import models
import json
from backend import sqltools
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    result = {}
    if request.method == 'GET':
        return render(request, "index.html")
    elif request.method == 'POST':
        prod = request.POST.get('product', '')
        env = request.POST.get('env', '')
        sql = request.POST.get('sql', '')
        database = request.POST.get('database', '')
        sql = sql.lower()
        if "limit" not in sql:
            result['message'] = "请添加limit限制返回条数"
            result['code'] = '300001'
            return HttpResponse(json.dumps(result))
        if prod == '' or env == '' or sql == '' or database == '':
            result['message'] = "The param prod or env or sql or database can not null"
            result['code'] = "300002"
            return HttpResponse(json.dumps(result))
        dbobj_list = models.SecretDB.objects.filter(name=database)
        if len(dbobj_list) > 0:
            result['message'] = "The database can not to select"
            result['code'] = "300004"
            return HttpResponse(json.dumps(result))
        if database == "exchange":
            sql_list = sql.split()
            if sql_list[3] == "pks":
                result['message'] = "The table can not to select"
                result['code'] = "300005"
                return HttpResponse(json.dumps(result))
        try:
            userobj = models.UserProfile.objects.get(product=prod, env=env)
            result = sqltools.select(userobj.mysql_host, userobj.mysql_port, userobj.mysql_user, userobj.mysql_pwd, sql, database)
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = str(e)
            result['code'] = "300006"
            return HttpResponse(json.dumps(result))


@csrf_exempt
def select_env(request):
    result = {}
    if request.method != "POST":
        result['message'] = "The method is not support"
        return HttpResponse(json.dumps(result))
    else:
        prod = request.POST.get('product', '')
        try:
            user_list = models.UserProfile.objects.filter(product=prod)
            result = [user.env for user in user_list]
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = "The product and env is not exists"
            result['code'] = "300003"
            return HttpResponse(json.dumps(result))


@csrf_exempt
def select_database(request):
    result = {}
    if request.method != "POST":
        result['message'] = "The method is not support"
        return HttpResponse(json.dumps(result))
    else:
        prod = request.POST.get('product', '')
        env = request.POST.get('env', '')
        try:
            userobj = models.UserProfile.objects.get(product=prod, env=env)
            result = sqltools.select_database(userobj.mysql_host, userobj.mysql_port, userobj.mysql_user, userobj.mysql_pwd)
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = "The product and env is not exists"
            result['code'] = "300003"
            return HttpResponse(json.dumps(result))
