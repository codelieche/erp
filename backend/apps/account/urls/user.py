# -*- coding:utf-8 -*-
from django.urls import path

from account.views.user import (
    UserCreateApiView,
    UserListView,
    UserAllListView,
    UserTuiguanListView,
    UserDetailView,
    UserChangePasswordApiView,
)


urlpatterns = [
    # 前缀：/api/v1/account/user/
    path('create', UserCreateApiView.as_view(), name="create"),
    path('password', UserChangePasswordApiView.as_view(), name="password"),
    path('list', UserListView.as_view(), name="list"),
    path('all', UserAllListView.as_view(), name="all"),
    path('tuiguan', UserTuiguanListView.as_view(), name="tuiguan"),
    path('<int:pk>', UserDetailView.as_view(), name="detail"),
    path('<str:username>', UserDetailView.as_view(lookup_field="username"), name="detail2"),
]
