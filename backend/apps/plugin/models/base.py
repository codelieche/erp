# -*- coding:utf-8 -*-
"""
基础插件
"""
from django.db import models
from django.utils import timezone

from codelieche.models import BaseModel


class Plugin(BaseModel):
    """
    插件，所有插件都继承自Plugin
    工作流的原子性是插件
    """
    # code = models.SlugField(verbose_name="插件名称", max_length=64, unique=True)
    # name = models.CharField(verbose_name="插件名称(中文)", max_length=128, blank=True, null=True)

    STATUS_CHOICES = (
        ("todo", "Todo"),
        ("doing", "进行中"),
        ("success", "成功"),
        ("error", "出错"),
        ("refuse", "拒绝"),
        ("cancel", "取消"),
        ("delete", "删除"),
        ("deliver", "转交"),
        ("agree", "通过"),
        ("done", "完成"),
    )

    # 插件信息
    PLUGIN_INFO = {
        "code": "plugin",   # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "插件",
        "description": "插件描述"
    }
    extra_methods = []   # 额外的方法，插件额外可执行的方法

    # 能执行核心任务的process状态，一般都是agree和sucess即可
    CAN_EXECUTE_CORE_TASK_STATUS = ["agree", "success"]
    # 接受从上一级步骤输入的字段, 当插件支持从上一个插件的核心任务返回的结果获取值时，我们可以设置这里
    RECEIVE_INPUT_FIELDS = ()

    # 核心任务是否已经执行完毕
    core_task_executed = models.BooleanField(verbose_name="核心任务是否已经执行", blank=True, default=False)
    # 状态
    status = models.CharField(verbose_name="状态", max_length=20, choices=STATUS_CHOICES,
                              blank=True, default="todo")
    time_updated = models.DateTimeField(verbose_name="更新时间", auto_now=True, blank=True)
    time_executed = models.DateTimeField(verbose_name="执行时间", blank=True, null=True)

    def entry_task(self, work, process, step):
        """
        进入任务
        :param work: 工作流实例
        :param process: 工作流的过程
        :param step: 工作流的步骤
        :return:
        """
        # 特殊情况，请自行覆盖本方法
        if process.auto:
            return self.core_task(work=work, process=process, step=step)
        else:
            # 这种情况一般是结合后续步骤的do_core_task_plugin来结合使用
            return process.entry_next_process()

    def execute_core_task(self, work=None):
        # 执行核心任务，我们应该返回3个值：
        # success(执行是否成功), result(执行结果的消息), output(输出给下一个步骤的数据)
        print("我是执行核心任务的函数，所有核心的操作可以放整个地方")
        raise NotImplementedError("请实现Execute Core Task方法")

    def core_task(self, work, process, step):
        # 可以考虑把这个设置为通用的方法
        results = self.execute_core_task(work=work)
        if len(results) == 3:
            success, result, output = results
        elif len(results) == 2:
            success, result = results
            output = None
        else:
            raise ValueError("插件{}返回的结果格式不正确".format(self))
        # 设置以及执行了
        self.core_task_executed = True
        now = timezone.datetime.now()
        self.time_executed = now  # 设置执行时间
        process.time_executed = now
        process.save()
        if success:
            self.status = "success"
        else:
            self.status = "error"
        # 对插件保存一下
        self.save()

        # 执行完毕，如果process.auto，那么我们要触发process的执行结果
        # 这是一个规范：如果不遵循，那么就没法自动跳入下一个步骤
        if process.auto:
            # 这里会直接进入下一个步骤（成功的情况下），出错了就直接error，整个流程也就报错
            process.handle_execute_result(success, result, output)

        # 返回执行结果
        return success, result, output

    class Meta:
        abstract = True
