# -*- coding:utf-8 -*-
from codelieche.views.viewset import ModelViewSet

from workflow.models.log import WorkFlowLog
from workflow.serializers.log import WorkflowLogModelSerializer


class WorkflowLogApiViewSet(ModelViewSet):
    """
    Workflow Log Api View Set
    """
    queryset = WorkFlowLog.objects.filter(deleted=False)
    serializer_class_set = (WorkflowLogModelSerializer,)

    search_fields = ("content", "workflow__title")
    filter_fields = ("category", "workflow")
