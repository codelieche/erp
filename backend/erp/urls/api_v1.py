# -*- coding:utf-8 -*-
from django.urls import path, include


urlpatterns = [
    # 前缀：/api/v1/
    path('account/', include(arg=("account.urls.api", "account"), namespace="account")),

    # CMDB相关的api
    path('cmdb/', include(arg=('cmdb.urls.api', 'cmdb'), namespace='cmdb')),

    # 配置相关的api
    path('config/', include(arg=("config.urls.api", "config"), namespace="config")),
    # Model日志相关的api
    path('modellog/', include(arg=('modellog.urls', 'modellog'), namespace='modellog')),

    # Utils相关的api
    path('utils/', include(arg=('utils.urls.api', 'utils'), namespace='utils')),
]
