# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from workflow.views.plugin.base import PluginsListApi
from workflow.views.flow import FlowApiModelViewSet
from workflow.views.step import StepApiModelViewSet
from workflow.views.workflow import WorkFlowApiModelViewSet
from workflow.views.process import ProcessApiModelViewSet
from workflow.views.log import WorkflowLogApiViewSet

router = DefaultRouter()
router.register("flow", FlowApiModelViewSet)
router.register("step", StepApiModelViewSet)
router.register("workflow", WorkFlowApiModelViewSet)
router.register("process", ProcessApiModelViewSet)
router.register("log", WorkflowLogApiViewSet)


urlpatterns = [
    # 前缀：/api/v1/workflow/
    path('plugins/', PluginsListApi.as_view(), name="plugins"),
    path('', include(router.urls), name="api"),
]

