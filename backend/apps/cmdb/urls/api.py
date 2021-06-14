# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cmdb.views.model import (
    ModelApiViewSet,
)
from cmdb.views.field import (
    FieldApiViewSet
)
from cmdb.views.instance import InstanceApiViewSet
from cmdb.views.value import ValueApiViewSet
from cmdb.views.permission import PermissionApiViewSet

router = DefaultRouter()
router.register('model', ModelApiViewSet)
router.register('field', FieldApiViewSet)
router.register('instance', InstanceApiViewSet)
router.register('value', ValueApiViewSet)
router.register('permission', PermissionApiViewSet)

urlpatterns = [
    # 前缀：/api/v1/cmdb/
    path('', include(router.urls), name="cmdb")
]
