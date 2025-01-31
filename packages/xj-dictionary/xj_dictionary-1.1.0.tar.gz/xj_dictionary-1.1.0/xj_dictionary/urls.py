# encoding: utf-8
"""
@project: djangoModel->url
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/6/6 14:25
"""

from django.urls import re_path, path

from .apis.dictionary_configure import DictionaryConfigure, DictionaryConfigurePage, BatchDictionaryConfigure

# 应用名称
app_name = 'xj_dictionary'

urlpatterns = [
    path("configure/<str:group>", DictionaryConfigure.as_view()),
    path("configure/<str:group>/<str:key>", DictionaryConfigure.as_view()),
    path("configure/<str:group>/<str:key>/<str:value>", DictionaryConfigure.as_view()),
    path("configure", DictionaryConfigure.as_view()),
    re_path("^list/?$", DictionaryConfigurePage.configure_page),  # 分页展示配置
    re_path("^groups/?$", BatchDictionaryConfigure.as_view()),  # TODO 暂时保留，后面将会去除掉该接口，批量搜索功能由上面接口代替
]
