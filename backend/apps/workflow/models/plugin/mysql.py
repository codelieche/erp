# -*- coding:utf-8 -*-
"""
执行MySQL的插件
"""
from django.db import models

from .base import Plugin
from workflow.models.workflow import WorkFlow


class MySQLPlugin(Plugin):
    """
    MySQL相关的插件
    主要是执行SQL的插件
    """
    PLUGIN_INFO = {
        "code": "mysql_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "MySQL插件",
        "description": "MySQL插件"
    }

    server = models.IntegerField(verbose_name="数据库服务")
    sql = models.TextField(verbose_name="SQL语句")
    database = models.CharField(verbose_name="数据库", max_length=128, blank=True, default=True)

    def entry_task(self, workflow, process, step):
        print("进入Mysql流程，我们直接进入下一步")
        process.entry_next_process()

    def execute_core_task(self):
        print("模拟执行MySQL插件的核心任务：当前sql为：{}".format(self.sql))
        return True, "执行成功"

    def core_task(self, workflow: WorkFlow, process, step):
        print("模拟执行MySQL插件的核心任务，当前workfow：{}".format(workflow))
        success, msg = self.execute_core_task()
        # 设置为已经执行了
        self.core_task_executed = True
        if success:
            self.status = "sucess"
            self.save()
            return True, "执行成功"
        else:
            self.status = "error"
            self.save()
            return False, msg

    class Meta:
        verbose_name = "MySQL插件"
        verbose_name_plural = verbose_name
