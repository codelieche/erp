# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.step import Step
from workflow.models.flow import Flow
from workflow.models.plugin import plugins_dict
from workflow.serializers.step import StepModelSerializer


class FlowModelSerializer(serializers.ModelSerializer):
    """
    流程Model Serializer
    """
    steps = StepModelSerializer(many=True, required=False, allow_null=True)

    def create_or_update_steps(self, flow: Flow, steps):
        """
        创建或者更新Flow的步骤
        """
        steps_list = []
        if steps and isinstance(steps, list) and len(steps) > 0:
            for item in steps:
                # 校验插件是否存在:
                step_id = item.get('id')
                plugin = item.get('plugin')
                name = item.get('name')
                stage = item.get('stage', 1)
                step_number = item.get('step', 1)
                data = item.get('data', "{}")
                auto_execute = item.get('auto_execute', False)

                if not plugin:
                    print("插件不可设置为空")
                    continue
                elif plugin not in plugins_dict:
                    print("当前系统不支持这个插件{}".format(plugin))
                    continue
                if step_id and step_id > 0:
                    # 更新步骤数据
                    step = Step.objects.filter(flow=flow, id=step_id, deleted=False)
                    if step:
                        # plugin是不可更新的
                        # 需要重新计算一下order
                        order = 10 ** stage + step_number
                        step.update(name=name, stage=stage, step=step_number, order=order, data=data,
                                    auto_execute=auto_execute)
                        # step.name = name
                        # step.stage = stage
                        # step.step = step_number
                        # step.data = data
                        # step.save()

                        steps_list.append(step.first())
                else:
                    # 创建新的步骤
                    step = Step.objects.create(
                        flow=flow, name=name, plugin=plugin,
                        stage=stage, step=step_number, data=data, auto_execute=auto_execute)
                    steps_list.append(step)
        # 返回步骤列表
        return steps_list

    def create(self, validated_data):
        # print(validated_data)
        # 1. 创建实例
        validated_data.pop('steps')
        instance = super().create(validated_data=validated_data)

        # 2. 添加相应的步骤
        steps = self.context['request'].data.get('steps')
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
