# -*- coding:utf-8 -*-
"""
项目流程相关的插件
项目插件，主要是创建项目，然后填写相关的参数
"""

from django.db import models

from .base import Plugin
# from workflow.models.work import Work


class ProjectCreatePlugin(Plugin):
    """
    项目创建的插件
    """
    PLUGIN_INFO = {
        "code": "project_create",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "项目创建插件",
        "description": "创建项目的插件"
    }

    code = models.SlugField(verbose_name="项目Code", max_length=128)
    name = models.CharField(verbose_name="项目名称", max_length=128)

    # def entry_task(self, work, process, step):
    #     print("进入Mysql流程，我们直接进入下一步")
    #     process.entry_next_process()

    def execute_core_task(self, work=None):
        print("执行项目插件的核心任务")
        return True, "执行成功", None

    # def core_task(self, work: Work, process, step):
    #     print("执行workfow:{}的核心任务".format(work))
    #     return True, "执行成功"

    class Meta:
        verbose_name = "项目创建"
        verbose_name_plural = verbose_name
