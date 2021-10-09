# -*- coding:utf-8 -*-
"""
作业流程的没一个过程
Flow配置的一个Step对应一个Process，可以转交的话，就对应多个了
"""
from django.db import models

from codelieche.models import BaseModel
from workflow.models.workflow import WorkFlow
from workflow.models.step import Step


class Process(BaseModel):
    """
    流程中的过程
    """
    flow = models.IntegerField(verbose_name="流程", blank=True, null=True)
    workflow = models.ForeignKey(verbose_name="流程实例", to=WorkFlow, blank=True, on_delete=models.CASCADE)
    step = models.ForeignKey(verbose_name="步骤", to=Step, blank=True, on_delete=models.CASCADE)
    plugin_id = models.IntegerField(verbose_name="插件实例的ID")
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)

    @property
    def plugin_obj(self):
        # 1. 获取到当前的插件对象
        plugin_class = self.step.plugin_class
        # 如果传递的plugin不存在就直接报错
        plugin = plugin_class.objects.get(id=self.plugin_id)

        # 如果插件不存在，直接出错
        return plugin

    def entry_task(self):
        # 进入这个process，可能是发短信，也可能是立刻进入下一个环节
        # 其实是调用插件实例的事件
        print("进入当前过程，处理事件")
        # 1. 获取到当前的插件对象
        # plugin_class = self.step.plugin_class
        # # 如果传递的plugin不存在就直接报错
        # plugin = plugin_class.objects.get(id=self.plugin_id)
        plugin = self.plugin_obj

        # 2. 执行插件的entry任务
        plugin.entry_task(workflow=self.workflow, process=self, step=self.step)

        # 3. 有些插件是直接进入下一个任务的

    def entry_next_process(self):
        # 1. 获取实例化Plugin所需的数据
        # 1-1：下一个任务
        next_step = self.workflow.get_next_step(current=self.step)

        # 修改一下状态
        if self.workflow.status == "todo":
            self.workflow.status = "doing"
            self.workflow.save()

        if not next_step:
            print(self, "没有下一个步骤了，无需执行")
            # 到这里应该是要检查一下workflow的状态了，比如全部修改成done
            self.workflow.status = "done"
            self.workflow.save()
            return
        # 1-2：下一个任务插件的数据
        success, plugin_data = WorkFlow.get_plugin_data(step=next_step, data=self.workflow.data)

        # 2. 创建插件
        if success and isinstance(plugin_data, dict):
            # plugin_class = next_step.plugin_class
            plugin_serializer_class = next_step.plugin_serializer_class
            # plugin_serializer_class(data=plugin_class)
            # plugin = plugin_class.objects.create(**plugin_data)

            serializer = plugin_serializer_class(data=plugin_data)
            if not serializer.is_valid():
                raise ValueError("实例化插件对象出错")

            plugin = serializer.save()
            print("实例化插件成功：", plugin)

            # 3. 实例化下一个process
            process = Process.objects.create(
                flow=self.flow, workflow=self.workflow, step=next_step, plugin_id=plugin.id)

            # 把workflow的当前process修改一下
            self.workflow.current = process.id
            # 记得保存一下
            self.workflow.save()

            # print("实例化下一个process成功：", process)
            # 触发进入这个流程的事件
            process.entry_task()  # 执行进入流程相关的事件

        else:
            raise ValueError("一般不会出现这个错误")

    def core_task(self):
        # 进入这个process的核心任务，可能是发短信，也可能是直接通过，进入下一个环节
        # 其实是调用插件实例的事件
        # print("进入当前过程，核心事件处理事件")
        # 1. 获取到当前的插件对象
        # plugin_class = self.step.plugin_class
        # # 如果传递的plugin不存在就直接报错
        # plugin = plugin_class.objects.get(id=self.plugin_id)
        plugin = self.plugin_obj

        # 2. 执行插件的核心任务
        # 2-1：判断是否可以进入核心任务
        if self.status in plugin.CAN_EXECUTE_CORE_TASK_STATUS:
            if plugin.core_task_executed:
                # print("当前插件的核心任务已经执行过了，不可执行")
                return False, "核心任务已经执行过了，不可继续执行"
            else:
                # if plugin.status not in ["todo2"]:
                #     return False, "当前插件状态不是todo不可执行"
                # 执行插件的核心任务：非常重要哦
                success, msg = plugin.core_task(workflow=self.workflow, process=self, step=self.step)

                # 考虑一下，这里是否需要修改process的状态
                return success, msg

        else:
            msg = "Process:{},当前状态({})不可以执行插件的核心任务".format(self, self.status)
            print(msg)
            return False, msg

        # 3. 有些插件是直接进入下一个任务的

    class Meta:
        verbose_name = "过程"
        verbose_name_plural = verbose_name
