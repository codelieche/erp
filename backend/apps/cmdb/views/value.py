# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from codelieche.views.viewset import ModelViewSet
from cmdb.models import Value
from cmdb.serializers import ValueModelSerializer


class ValueApiViewSet(ModelViewSet):
    """
    资产实例信息值 Api
    """
    queryset = Value.objects.filter(deleted=False)
    serializer_class = ValueModelSerializer
    serializer_class_set = (ValueModelSerializer,)
    permission_classes = (IsAuthenticated,)

    search_fields = ('model__code', 'field__code', 'value')
    filter_fields = (
        'instance', 'model', 'model__code', 'field', 'field__code', 'deleted',
    )
    orderring_fields = ('id', 'instance', 'model', 'field', 'deleted', 'time_added')
    ordering = ('instance', 'field', 'id')

