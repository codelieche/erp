# -*- coding:utf-8 -*-
import json

from rest_framework import serializers

from workflow.models.plugin import plugins_dict
from workflow.serializers.plugin import plugin_serializers_mapping
from workflow.models.flow import Flow
from workflow.models.workflow import WorkFlow
from workflow.models.process import Process
from workflow.models.log import WorkFlowLog
from workflow.serializers.process import ProcessInfoModelSerializer


class WorkFlowModelSerializer(serializers.ModelSerializer):
    """
    Workflow Model Serializer
    """

    def check_plugin_data(self, flow: Flow, data):
        # print("开始校验插件所需的数据")

        # 1. 校验流程和步骤
        if not flow:
             raise serializers.ValidationError("传入的flow不正确")

        steps = flow.steps
        if not steps:
            raise serializers.ValidationError("当前流程的步骤为空，不可发起流程")

        # 2. 开始校验每一步的数据
        for step in steps:
            # print("校验步骤：{}-{}".format(step, step.plugin))
            # 2-1: 取出插件序列化类
            plugin_name = step.plugin
            serailizer_class = plugin_serializers_mapping.get(plugin_name)
            if not serailizer_class:
                raise serializers.ValidationError("序列化还不支持插件{}".format(plugin_name))

            # 2-2：取出初始化插件的数据
            plugin_data = {}
            success, result = WorkFlow.get_plugin_data(step, data)
            if not success or not isinstance(result, dict):
                raise serializers.ValidationError(result)
            else:
                plugin_data = result

            # 2-2-1：先准备个dict
            # plugin_data = {}
            # 2-2-2：从step配置的数据中获取
            # if step.data:
            #     if isinstance(step.data, str):
            #         try:
            #             step_plugin_data = json.loads(step.data)
            #             plugin_data.update(step_plugin_data)
            #         except Exception as e:
            #             msg = "步骤(id:{})配置的初始化数据有误".format(step.id)
            #             raise serializers.ValidationError(msg)
            #     elif isinstance(step.data, dict):
            #         plugin_data.update(step.data)
            # # 2-2-3：从传递的data中获取
            # step_data_key = "step_{}".format(step.id)
            # step_data = data.get(step_data_key)
            # if step_data:
            #     if isinstance(step_data, str):
            #         try:
            #             step_plugin_data = json.loads(step.data)
            #             plugin_data.update(step_plugin_data)
            #         except Exception as e:
            #             msg = "步骤(id:{})配置的初始化数据有误".format(step_data_key)
            #             raise serializers.ValidationError(msg)
            #     elif isinstance(step_data, dict):
            #         plugin_data.update(step_data)

            # 2-3: 校验当前步骤插件的数据
            serializer = serailizer_class(data=plugin_data)
            if not serializer.is_valid():
                msg = "step_{}校验{}插件数据有误{}".format(step.id, plugin_name, serializer.errors)
                raise serializers.ValidationError(msg)

        # raise serializers.ValidationError("校验插件数据失败")

    def create(self, validated_data):
        # 1. 校验data是否OK
        flow = validated_data['flow']
        data = validated_data.get('data')
        self.check_plugin_data(flow, data)

        # 2. 调用父类的创建方法
        # print(validated_data)
        instance = super().create(validated_data=validated_data)
        # 记录日志：创建成功
        user = self.context['request'].user
        content = "{}创建流程成功".format(user.username)
        WorkFlowLog.objects.create(workflow_id=instance.id, user=user.username, category="info", content=content)

        # 3. 初始化第一个步骤的process
        # 3-1: 获取到step
        step = flow.steps.first()
        if not step:
            raise serializers.ValidationError("一般不会出现这个情况，flow一般都是有步骤的")
        plugin_class = plugins_dict.get(step.plugin)
        if not plugin_class:
            raise serializers.ValidationError("一般也不会出现这情况，flow配置的插件不存在")

        # 3-2：获取到插件实例化所需的数据
        success, plugin_data = WorkFlow.get_plugin_data(step=step, data=instance.data)

        # 3-3: 创建插件
        if success and isinstance(plugin_data, dict):
            plugin = plugin_class.objects.create(**plugin_data)
            # print("实例化插件成功：", plugin)
            # 3-4：实例化process, 且第一步process状态直接设置为成功
            process = Process.objects.create(
                flow=instance.flow_id, workflow=instance, step=step,
                plugin_id=plugin.id, status="success",
                auto_execute=step.auto_execute,
            )
            # 保存一下当前流程实例的当前步骤
            instance.current = process.id
            instance.save()

            # print("实例化第一个process成功：", process)
            # 触发进入这个流程的事件
            process.entry_task()   # 执行进入流程相关的事件

        else:
            raise serializers.ValidationError("一般不会出现这个错误")

        return instance

    class Meta:
        model = WorkFlow
        fields = (
            "id", "flow", "title",
            "status", "status_code",
            "user", "current", "data",
            "time_added", "time_finished",
        )


class WorkflowInfoModelSerializer(serializers.ModelSerializer):

    process_set = ProcessInfoModelSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = WorkFlow
        fields = (
            "id", "flow", "title",
            "status", "status_code",
            "user", "current", "data", 'process_set',
            "time_added", "time_finished",
        )
