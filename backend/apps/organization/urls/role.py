# -*- coding:utf-8 -*-

from django.urls import path

from organization.views.role import (
    RoleCreateApiView,
    RoleListApiView,
    RoleAllListApiView,
    RoleDetailApiView
)


urlpatterns = [
    # 前缀：/api/v1/serializer/role/
    path("create", RoleCreateApiView.as_view(), name="create"),
    path("list", RoleListApiView.as_view(), name="list"),
    path("all", RoleAllListApiView.as_view(), name="all"),
    path("<int:pk>", RoleDetailApiView.as_view(), name="detail")
]
