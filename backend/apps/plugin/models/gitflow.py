# -*- coding:utf-8 -*-
"""
这个是代码提交相关的插件
"""

from django.db import models

from .base import Plugin


class GitFlowPlugin(Plugin):
    """
    Git代码提交相关的插件
    主要是模拟提交代码相关的操作
    """

    PLUGIN_INFO = {
        "code": "gitflow_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "Gitflow插件",
        "description": "Gitflow插件",
    }
    # 从配置的Gitlab中选择服务：我们可以从中获取到url、code等所需的信息
    gitlabl = models.IntegerField(verbose_name="Git仓库")
    project = models.CharField(verbose_name="项目", max_length=256)
    branch = models.CharField(verbose_name="代码分支", max_length=128)
    commit = models.CharField(verbose_name="提交ID", blank=True, null=True, max_length=128)

    # def entry_task(self, work, process, step):
    #     print("进入Gitflow插件：")
    #     if process.auto_execute:
    #         self.core_task(work=work, process=process, step=step)
    #     else:
    #         # 这种情况一般是结合后续步骤的do_core_task_plugin来结合使用
    #         process.entry_next_process()

    def execute_core_task(self, work=None):
        print("执行GitFlow核心任务：branch:{}-{}".format(self.branch, self.commit))
        print("现在开始获取gitlab服务信息:{}".format(self.gitlabl))
        print("现在开始获取gitlab项目信息:{}".format(self.project))
        print("现在开始拉取代码:{}-{}".format(self.branch, self.commit))
        return True, "执行成功", None

    # def core_task(self, work: Work, process, step):
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
