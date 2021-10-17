# -*- coding:utf-8 -*-
from rest_framework import serializers

from plugin.models import plugins_dict
from plugin.serializers import plugin_serializers_mapping
from workflow.models.process import Process
from workflow.serializers.step import StepModelSerializer
from workflow.serializers.result import ProcessResultModelSerializer


class ProcessModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Process
        fields = (
            "id", "flow_id", "step_id", "work_id",
            "status", "auto", "time_executed"
        )


class ProcessInfoModelSerializer(serializers.ModelSerializer):

    step = StepModelSerializer(read_only=True, allow_null=True)
    result = ProcessResultModelSerializer(read_only=True, allow_null=True)
    plugin = serializers.SerializerMethodField(read_only=True, allow_null=True)

    def get_plugin(self, obj):
        # 获取插件的序列化对象
        if not obj.plugin_id:
            return None

        try:
            # 1. 获取到插件的类和插件对象
            plugin_name = obj.step.plugin
            plugin_class = plugins_dict.get(plugin_name)

            if plugin_class and obj.plugin_id:
                plugin_obj = plugin_class.objects.get(pk=obj.plugin_id)

                # 2. 获取到插件序列化类
                plugin_serializer_class = plugin_serializers_mapping.get(plugin_name)
                if plugin_serializer_class:
                    # 3. 返回序列化对象
                    plugin_serializer = plugin_serializer_class(plugin_obj)
                    return plugin_serializer.data
            else:
                return None
        except Exception as e:
            print("获取过程(ID:{})的插件对象出错".format(obj.id))
            return None

    class Meta:
        model = Process
        fields = (
            "id", "flow_id", "step_id", "step", "plugin_id", "plugin",
            "work_id", "result", "status", "auto", "time_executed"
        )
