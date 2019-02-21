# -*- coding:utf-8 -*-
from django.urls import path, include

urlpatterns = [
    # 前缀：/api/v1/
    # account api
    path('account/', include(arg=("account.urls.api", "account"), namespace="account")),

    # Model日志相关的api
    path('modellog/', include(arg=('modellog.urls', 'modellog'), namespace='modellog')),
    # util api
    path('utils/', include(arg=("utils.urls.api", "utils"), namespace="utils")),

]
