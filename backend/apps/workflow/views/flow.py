# -*- coding:utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import action

from codelieche.views.viewset import ModelViewSet
from workflow.models.flow import Flow
from workflow.models.work import Work
from workflow.serializers.flow import FlowModelSerializer, FlowSimpleModelSerializer
from workflow.serializers.work import WorkModelSerializer


class FlowApiModelViewSet(ModelViewSet):
    """
    Flow Api View Set
    """
    queryset = Flow.objects.filter(deleted=False)
    serializer_class_set = (FlowModelSerializer, FlowSimpleModelSerializer)

    @action(methods=["GET"], detail=True, description="工作流实例列表")
    def work(self, request, pk=None):
        user = request.user
        flow = self.get_object()

        if user.is_superuser:
            queryset = Work.objects.filter(flow_id=flow.id, deleted=False)
        else:
            queryset = Work.objects.filter(flow_id=flow.id, deleted=False, user_id=user.id)

        # 分页处理
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WorkModelSerializer(data=page, many=True)
            serializer.is_valid()
            return self.get_paginated_response(serializer.data)
        else:
            # 返回全部的数据
            works = queryset.all()
            serializer = WorkModelSerializer(works, many=True)
            return Response(data=serializer.data)
