# -*- coding:utf-8 -*-

from django.urls import path

from organization.views.category import (
    CategoryCreateApiView,
    CategoryListApiView,
    CategoryAllListApiView,
    CategoryDetailApiView
)


urlpatterns = [
    # 前缀：/api/v1/serializer/category/
    path("create", CategoryCreateApiView.as_view(), name="create"),
    path("list", CategoryListApiView.as_view(), name="list"),
    path("all", CategoryAllListApiView.as_view(), name="all"),
    path("<int:pk>", CategoryDetailApiView.as_view(), name="detail")
]
