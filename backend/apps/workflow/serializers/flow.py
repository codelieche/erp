# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.step import Step
from workflow.models.flow import Flow
from plugin.models import plugins_dict
from workflow.serializers.step import StepModelSerializer


class FlowModelSerializer(serializers.ModelSerializer):
    """
    流程Model Serializer
    其实需要检查流程是否合理，比如未设置自动执行的插件，它是否配置了do_core_task_plugin的插件
    """
    steps = StepModelSerializer(many=True, required=False, allow_null=True)

    def create_or_update_steps(self, flow: Flow, steps):
        """
        创建或者更新Flow的步骤
        """
        steps_list = []
        if steps and isinstance(steps, list) and len(steps) > 0:
            # 先检查一下步骤是否设置的合理
            need_do_core_task_plugin = False
            for item in steps:
                # 有可能插件是删除了的，我们就跳过一下
                step_id = item.get('id')
                if step_id and step_id > 0:
                    # 更新步骤数据
                    step = Step.objects.filter(flow_id=flow.id, id=step_id, deleted=False)
                    if not step:
                        # 如果插件不存在，就跳过
                        continue

                # 对插件进行判断
                if item.get('plugin') != "do_core_task_plugin":
                    auto_execute = item.get('auto_execute', False)
                    if auto_execute is True or auto_execute == 1:
                        if not need_do_core_task_plugin:
                            # 如果前面的插件需要do_core_task_plugin，那么这里依然不可设置为False
                            need_do_core_task_plugin = False
                    else:
                        need_do_core_task_plugin = True
                else:
                    need_do_core_task_plugin = False

            # 最后遍历完毕发现，还需要need_do_core_task_plugin那么就报错
            if need_do_core_task_plugin:
                raise serializers.ValidationError("我需要do_core_task_plugin结尾，请重新组合插件")

            for item in steps:
                # 校验插件是否存在:
                step_id = item.get('id')
                plugin = item.get('plugin')
                name = item.get('name')
                stage = item.get('stage', 1)
                step_number = item.get('step', 1)
                data = item.get('data', "{}")
                auto_execute = item.get('auto_execute', False)
                receive_input = item.get('receive_input', False)  # 是否接受上一步的输出作为这一步插件的输入

                if not plugin:
                    print("插件不可设置为空")
                    continue

                elif plugin not in plugins_dict:
                    print("当前系统不支持这个插件{}".format(plugin))
                    continue

                if step_id and step_id > 0:
                    # 更新步骤数据
                    step = Step.objects.filter(flow_id=flow.id, id=step_id, deleted=False)
                    if step:
                        # plugin是不可更新的
                        # 需要重新计算一下order
                        order = 10 ** stage + step_number
                        step.update(
                            name=name, stage=stage, step=step_number, order=order, data=data,
                            auto_execute=auto_execute, receive_input=receive_input
                        )
                        # step.name = name
                        # step.stage = stage
                        # step.step = step_number
                        # step.data = data
                        # step.save()

                        steps_list.append(step.first())
                else:
                    # 如果传入了flow就创建新的步骤
                    if flow:
                        step = Step.objects.create(
                            flow_id=flow.id, name=name, plugin=plugin,
                            stage=stage, step=step_number, data=data,
                            auto_execute=auto_execute, receive_input=receive_input
                        )
                        steps_list.append(step)
        # 返回步骤列表
        return steps_list

    def create(self, validated_data):
        # print(validated_data)
        # 1. 创建实例
        # 1.1 检查传入的steps是否正确，主要是检查组合是否合理
        steps = self.context['request'].data.get('steps')
        self.create_or_update_steps(flow=None, steps=steps)

        # 1.2 检查步骤ok，就可创建流程了
        user = self.context["request"].user
        validated_data['user_id'] = user.id
        validated_data.pop('steps')
        instance = super().create(validated_data=validated_data)

        # 2. 添加相应的步骤
        self.create_or_update_steps(flow=instance, steps=steps)

        # 3. 返回对象
        return instance

    def update(self, instance, validated_data):
        # 1. 先剥离出steps
        validated_data.pop('steps')
        instance = super().update(instance=instance, validated_data=validated_data)

        # 2. 更新步骤数据：注意删除step请单独删除
        steps = self.context['request'].data.get('steps')
        if steps:
            steps_list = self.create_or_update_steps(flow=instance, steps=steps)
            # 遍历一下，如果不在当前steps_list里面的步骤就删除
            steps_ids = [i.id for i in steps_list]
            # 遍历flow的所有步骤，不在新的steps_list中的就删除
            for step in instance.steps:
                if step.id not in steps_ids:
                    step.delete()

        # 3. 返回对象
        return instance

    class Meta:
        model = Flow
        fields = ("id", "code", "name", "user", "steps")


class FlowSimpleModelSerializer(serializers.ModelSerializer):
    """流程简单的数据序列化"""
    
    class Meta:
        model = Flow
        fields = ("id", "code", "name")
