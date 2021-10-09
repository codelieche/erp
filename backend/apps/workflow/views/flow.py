# -*- coding:utf-8 -*-

from codelieche.views.viewset import ModelViewSet
from workflow.models.flow import Flow
from workflow.serializers.flow import FlowModelSerializer


class FlowApiModelViewSet(ModelViewSet):
    """
    Flow Api View Set
    """
    queryset = Flow.objects.filter(deleted=False)
    serializer_class_set = (FlowModelSerializer,)
