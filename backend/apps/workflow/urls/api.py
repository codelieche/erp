# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from plugin.views.base import PluginsListApi
from workflow.views.flow import FlowApiModelViewSet
from workflow.views.step import StepApiModelViewSet
from workflow.views.work import workApiModelViewSet
from workflow.views.process import ProcessApiModelViewSet
from workflow.views.log import WorkLogApiViewSet

router = DefaultRouter()
router.register("flow", FlowApiModelViewSet)
router.register("step", StepApiModelViewSet)
router.register("work", workApiModelViewSet)
router.register("process", ProcessApiModelViewSet)
router.register("log", WorkLogApiViewSet)


urlpatterns = [
    # 前缀：/api/v1/work/
    path('plugins/', PluginsListApi.as_view(), name="plugins"),
    path('', include(router.urls), name="api"),
]

