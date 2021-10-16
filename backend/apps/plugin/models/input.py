# -*- coding:utf-8 -*-
"""
这个是构建Output Input相关的插件示例
"""
import time
import datetime

from django.db import models

from .base import Plugin


class InputOutputPlugin(Plugin):
    """
    输入输出的插件示例
    主要是模拟插件的输出，作为下一个插件的输入
    """

    PLUGIN_INFO = {
        "code": "input_output_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "输入输出插件",
        "description": "输入输出插件",
    }

    RECEIVE_INPUT_FIELDS = ("value",)
    # 从配置的Jenkins中选择服务：我们可以从中获取到url、username、password等所需的信息
    value = models.CharField(verbose_name="输入值", max_length=1024, blank=True, null=True)

    def execute_core_task(self, work=None):
        print("执行InputPlugin(ID:{})核心任务：{}".format(self.id, self.value))
        for i in range(10):
            print("执行输入输出插件核心任务：{}".format(i + 1))
            time.sleep(0.25)
        now = datetime.datetime.now().strftime("%F %T")
        output = {
            "value": "{}-{}\n".format(self.value, now)
        }
        return True, "执行成功", output
