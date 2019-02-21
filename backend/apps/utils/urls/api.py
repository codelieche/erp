# -*- coding:utf-8 -*-
"""
工具相关的api路由
"""

from django.urls import path

from utils.views.permissions import CheckUserPermissionApiView


urlpatterns = [
    # 前缀：/api/v1/utils/
    path("check/permission", CheckUserPermissionApiView.as_view(), name="check_permission"),
]
