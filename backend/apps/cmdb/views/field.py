# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from codelieche.views.viewset import ModelViewSet
from cmdb.models import Field
from cmdb.serializers import FieldModelSerializer


class FieldApiViewSet(ModelViewSet):
    """
    资产模型Field Api
    """
    queryset = Field.objects.filter(deleted=False)
    serializer_class = FieldModelSerializer
    serializer_class_set = (FieldModelSerializer,)
    permission_classes = (IsAuthenticated,)

    search_fields = ('name', 'code',)
    filter_fields = ('model', 'model__code', 'deleted', 'db_index', 'unique', 'multi')
    orderring_fields = ('id', 'model', 'code', 'deleted', 'time_added')
    ordering = ('model', 'id')


