# -*- coding:utf-8 -*-
from codelieche.views.viewset import ReadOnlyViewSet

from workflow.models.log import WorkFlowLog
from workflow.serializers.log import WorkflowLogModelSerializer


class WorkflowLogApiViewSet(ReadOnlyViewSet):
    """
    Workflow Log Api View Set
    """
    queryset = WorkFlowLog.objects.filter(deleted=False)
    serializer_class_set = (WorkflowLogModelSerializer,)

    search_fields = ("content",)
    filter_fields = ("category", "workflow_id")

