# -*- coding:utf-8 -*-
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from codelieche.views.viewset import ModelViewSet
from cmdb.models import Permission
from cmdb.serializers.permission import (
    PermissionModelSerializer, PermissionInfoModelSerializer
)


class PermissionApiViewSet(ModelViewSet):
    """
    资产模型Field Api
    """
    queryset = Permission.objects.filter(deleted=False)
    serializer_class = PermissionModelSerializer
    serializer_class_set = (PermissionModelSerializer, PermissionInfoModelSerializer)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    search_fields = ('name', 'group__name',)
    filter_fields = ('groups', 'model', 'instances', 'deleted')
    orderring_fields = ('id', 'can_view_all', 'deleted', 'time_added')
    ordering = ('id',)
