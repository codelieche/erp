# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from codelieche.views.viewset import ModelViewSet
from cmdb.models import Model
from cmdb.serializers import ModelSerializer


class ModelApiViewSet(ModelViewSet):
    """
    资产模型 Api
    """
    queryset = Model.objects.filter(deleted=False)
    serializer_class = ModelSerializer
    serializer_class_set = (ModelSerializer,)
    permission_classes = (IsAuthenticated,)

    search_fields = ('name', 'code',)
    orderring_fields = ('id', 'deleted', 'time_added')
    filter_fields = ('deleted',)