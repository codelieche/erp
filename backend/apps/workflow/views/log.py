# -*- coding:utf-8 -*-
from codelieche.views.viewset import ReadOnlyViewSet

from workflow.models.log import WorkLog
from workflow.serializers.log import WorkLogModelSerializer


class WorkLogApiViewSet(ReadOnlyViewSet):
    """
    work Log Api View Set
    """
    queryset = WorkLog.objects.filter(deleted=False)
    serializer_class_set = (WorkLogModelSerializer,)

    search_fields = ("content",)
    filter_fields = ("category", "work_id")

