# -*- coding:utf-8 -*-
from codelieche.views.viewset import ModelViewSet
from workflow.models.process import Process
from workflow.serializers.process import ProcessModelSerializer, ProcessInfoModelSerializer


class ProcessApiModelViewSet(ModelViewSet):
    """
    Process Api Model View Set
    """
    queryset = Process.objects.filter(deleted=False)
    serializer_class_set = (ProcessModelSerializer, ProcessInfoModelSerializer)

    search_fields = ("workflow__title",)
    filter_fields = ("flow", "workflow", "status")
