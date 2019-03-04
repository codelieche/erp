# -*- coding:utf-8 -*-

from django.urls import path, include


urlpatterns = [
    # 前缀：/api/v1/serializer/
    # 分类
    path("category/", include(arg=("organization.urls.category", "organization"), namespace="category")),
    # 角色
    path("role/", include(arg=("organization.urls.role", "organization"), namespace="role")),
]
