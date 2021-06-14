# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from codelieche.views.viewset import ModelViewSet
from cmdb.models import Instance
from cmdb.serializers import InstanceModelSerializer


class InstanceApiViewSet(ModelViewSet):
    """
    资产模型实例 Api
    """
    queryset = Instance.objects.filter(deleted=False)
    serializer_class = InstanceModelSerializer
    serializer_class_set = (InstanceModelSerializer,)
    permission_classes = (IsAuthenticated,)

    search_fields = ('model__code', 'model__name',)
    filter_fields = (
        'model', 'model__code', 'deleted',
    )
    orderring_fields = ('id', 'model', 'deleted', 'time_added')
    ordering = ('model', 'id')

