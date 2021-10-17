# -*- coding:utf-8 -*-
from rest_framework import serializers
from workflow.models.step import Step


class StepModelSerializer(serializers.ModelSerializer):
    """
    Step Model Serializer
    """

    class Meta:
        model = Step
        fields = (
            "id", "name", "plugin", "stage", "step", "order", "data",
            "auto", "receive_input"
        )
