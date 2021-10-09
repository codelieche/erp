# -*- coding:utf-8 -*-

from codelieche.views.viewset import ModelViewSet
from workflow.models.step import Step
from workflow.serializers.step import StepModelSerializer


class StepApiModelViewSet(ModelViewSet):
    """
    Step Api View Set
    """
    queryset = Step.objects.filter(deleted=False)
    serializer_class_set = (StepModelSerializer,)
