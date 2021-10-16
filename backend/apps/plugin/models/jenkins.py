# -*- coding:utf-8 -*-
"""
这个是构建Jenkins相关的插件
"""

from django.db import models

from .base import Plugin
# from workflow.models.workflow import WorkFlow


class JenkinsPlugin(Plugin):
    """
    Jenkins构建相关的插件
    主要是模拟Jenkins构建相关的操作
    """

    PLUGIN_INFO = {
        "code": "jenkins_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "Jenkins插件",
        "description": "Jenkins插件",
    }
    # 从配置的Jenkins中选择服务：我们可以从中获取到url、username、password等所需的信息
    jenkins = models.IntegerField(verbose_name="Jenkins服务")
    job = models.CharField(verbose_name="Job", max_length=256)
    params = models.JSONField(verbose_name="构建参数", blank=True, null=True)
    build_id = models.IntegerField(verbose_name="构建ID", blank=True, null=True)

    # def entry_task(self, workflow, process, step):
    #     print("进入Jenkins插件：")
    #     if process.auto_execute:
    #         self.core_task(workflow=workflow, process=process, step=step)
    #     else:
    #         # 这种情况一般是结合后续步骤的do_core_task_plugin来结合使用
    #         process.entry_next_process()

    def execute_core_task(self, workflow=None):
        print("执行Jenkins核心任务：{}-{}-{}".format(self.jenkins, self.job, self.params))
        print("现在开始获取Jenkins服务信息:{}".format(self.jenkins))
        print("现在开始获取Job信息:{}".format(self.job))
        print("现在开始构建Job:{}-{}".format(self.job, self.params))
        return True, "执行成功", None

    # def core_task(self, workflow: WorkFlow, process, step):
    #     # 可以考虑把这个设置为通用的方法
    #     success, result = self.execute_core_task()
    #     # 设置以及执行了
    #     self.core_task_executed = True
    #     if success:
    #         self.status = "success"
    #     else:
    #         self.status = "error"
    #     # 对插件保存一下
    #     self.save()
    #
    #     # 执行完毕，如果process.auto_execute，那么我们要触发process的执行结果
    #     # 这是一个规范：如果不遵循，那么就没法自动跳入下一个步骤
    #     if process.auto_execute:
    #         # 这里会直接进入下一个步骤（成功的情况下），出错了就直接error，整个流程也就报错
    #         process.handle_execute_result(success, result)
    #
    #     # 返回执行结果
    #     return success, result
