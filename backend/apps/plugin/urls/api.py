# -*- coding:utf-8 -*-
from django.urls import path

from plugin.views.base import PluginsListApi


urlpatterns = [
    # 前缀：/api/v1/plugin
    path('plugins/', PluginsListApi.as_view(), name="plugins"),
]
