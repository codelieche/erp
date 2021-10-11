# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.log import WorkFlowLog


class WorkflowLogModelSerializer(serializers.ModelSerializer):
    """
    Workflow Log Model Serializer
    """

    class Meta:
        model = WorkFlowLog
        fields = (
            "id", "workflow_id", "category", "content"
        )
