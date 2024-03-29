# -*- coding:utf-8 -*-
"""
执行MySQL的插件
"""
from django.db import models

from .base import Plugin
# from workflow.models.work import Work


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

    # def entry_task(self, work, process, step):
    #     if process.auto:
    #         self.core_task(work=work, process=process, step=step)
    #     else:
    #         print("进入Mysql流程，我们直接进入下一步")
    #         # 这种情况一般是结合后续步骤的do_core_task_plugin来结合使用
    #         process.entry_next_process()

    def execute_core_task(self, work=None):
        print("模拟执行MySQL插件的核心任务：当前sql为：{}".format(self.sql))
        for i in range(10):
            print("模拟执行SQL:{}".format(i + 1))
        return True, "执行成功", None

    # def core_task(self, work: Work, process, step):
    #     print("模拟执行MySQL插件的核心任务，当前workfow：{}".format(work))
    #     success, result = self.execute_core_task()
    #     # 设置为已经执行了
    #     self.core_task_executed = True
    #     if success:
    #         self.status = "sucess"
    #         self.save()
    #     else:
    #         self.status = "error"
    #         self.save()
    #
    #     # 执行完毕，如果process.auto，那么我们要触发process的执行结果
    #     # 这是一个规范：如果不遵循，那么就没法自动跳入下一个步骤
    #     if process.auto:
    #         # 里面会直接进入下一步
    #         process.handle_execute_result(success, result)
    #
    #     # 返回执行结果
    #     return success, result

    class Meta:
        verbose_name = "MySQL插件"
        verbose_name_plural = verbose_name
