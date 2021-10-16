# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.log import WorkLog


class WorkLogModelSerializer(serializers.ModelSerializer):
    """
    work Log Model Serializer
    """

    class Meta:
        model = WorkLog
        fields = (
            "id", "work_id", "category", "content"
        )
