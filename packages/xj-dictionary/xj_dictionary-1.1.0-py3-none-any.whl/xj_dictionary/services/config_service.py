# -*- coding: UTF-8 -*-
"""
@project: djangoModel->service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/6/6 14:23
"""

from django.core.cache import cache
from django.core.paginator import PageNotAnInteger, EmptyPage

from .. import models
# import datetime
from ..utils.custom_tool import format_params_handle, filter_fields_handler
# from django.conf import settings
# from django.utils import timezone
# from django.core.cache import cache
from ..utils.model_handle import *


# def getConfigRouter():
# 	domain = router.getSiteDomain()
# 	return settings.DATABASE_MAPPING.get(domain, domain)
# # end - getConfigRouter


# cache 不支持异步
def getConfig(group=None, key=None):
    ch = cache.get('dictionary_configure')
    if not ch:
        ch = updateConfig()
    if not group:
        return ch
    if group in ch:
        if not key:
            return ch[group]
        if key in ch[group]:
            return ch[group][key]
    # end if

    return None


# end - getConfig


def updateConfig(group=None, key=None, value=None):
    ch = (cache.get('dictionary_configure') or {}) if group else {}
    if not ch or not group:
        for kv in models.Configure.objects.all():
            if str(kv.group) not in ch:
                ch[str(kv.group)] = {}
            ch[str(kv.group)][str(kv.key)] = str(kv.value)
        # end for
    elif group and key and value:
        if str(group) not in ch:
            ch[str(group)] = {}

        ch[str(group)][str(key)] = str(value)
    elif group and key:
        if str(group) not in ch:
            ch[str(group)] = {}

        try:
            ch[str(group)][str(key)] = str(models.Configure.objects.get(group=group, key=key).value)
        except:
            pass
        # end try
    elif group:
        if str(group) not in ch:
            ch[str(group)] = {}

        for kv in models.Configure.objects.filter(group=group):
            ch[str(group)][str(kv.key)] = str(kv.value)
        # end for
    # end if

    # cache.set("Config_{}".format(getConfigRouter()), ch)
    return ch


# end - updateConfig


def getPricing(province, hurry, key="邮费"):
    priceBase = None
    if province:
        priceBase = getConfig(key, province)
    if not priceBase and province:
        priceBase = getConfig(key, "其他省份")
    if not priceBase:
        priceBase = "0.0"

    price = float(priceBase)

    if hurry:
        priceHurry = getConfig(key, "当日加急")
        if priceHurry:
            price += float(priceHurry)
    # end if

    return price


# end - getPricing


# 创建配置
def setConfig(group, key, value, description):
    models.Configure.objects.update_or_create(
        group=group, key=key,
        defaults={"value": value, "description": description}
    )

    updateConfig()


# end - setConfig


# 配置删除
def delConfig(request):
    key = request.data.get('key', None)
    group = request.data.get('group', None)
    if not group or not key:
        return util_response(err=4055, msg="参数错误")
    res = models.Configure.objects.filter(group=group, key=key)
    if res:
        res.delete()
        return util_response()
    else:
        return util_response(err=2254, msg="该配置不存在")


# def getAdvert():
# 	return cache.get("Advert_{}".format(getConfigRouter())) or updateAdvert()
# #end - getAdvert
#
# def updateAdvert():
# 	data = {}
# 	for ad in models.Advert.objects.filter(expire__gte=timezone.now()).order_by("-sort"):
# 		if ad.location not in data:
# 			data[ad.location] = []
# 		data[ad.location].append({ "url" : ad.url, "img" : "{}{}".format(settings.MEDIA_URL, ad.image), "hint" : ad.hint })
# 	#end for
#
# 	cache.set("Advert_{}".format(getConfigRouter()), data)
# 	return data
# #end - updateAdvert


# 配置列表综合查询
def dictionary_configure_list(filter_fields_params=None, filter_fields=None, need_pagination=True):
    """
    类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
     """
    # 参数筛选
    if filter_fields_params is None:
        filter_fields_params = {}

    page = filter_fields_params.pop("page", 1)
    size = filter_fields_params.pop("size", 10)

    # 查询参数过滤，替换
    filter_fields_params = format_params_handle(
        param_dict=filter_fields_params,
        filter_filed_list=["id", "group", "key", "group_list", "id_list", "key_list"],
        alias_dict={"id_list": "id__in", "group_list": "group__in", "key_list": "key__in"}
    )

    # 查询字段筛选
    default_fields = ["group", "key", "value", "description", "icon"]
    filter_fields_list = filter_fields_handler(
        default_field_list=default_fields,
        input_field_expression=filter_fields,
        all_field_list=default_fields
    )

    # 数据库orm查询
    dictionary_configure_obj = models.Configure.objects.filter(**filter_fields_params).order_by("group").values(*filter_fields_list)

    # 不需要分页展示全部数据
    if not need_pagination:
        if not dictionary_configure_obj:
            return [], None
        return list(dictionary_configure_obj), None

    # 分页展示
    count = dictionary_configure_obj.count()
    paginator = Paginator(dictionary_configure_obj, size)
    try:
        thread_tag_obj = paginator.page(page)
    except PageNotAnInteger:
        thread_tag_obj = paginator.page(1)
    except EmptyPage:
        thread_tag_obj = paginator.page(paginator.num_pages)

    finish_set = list(thread_tag_obj.object_list)
    return {'size': int(size), 'page': int(page), 'total': count, 'list': finish_set}, None
