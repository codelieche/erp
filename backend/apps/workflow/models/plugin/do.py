# -*- coding:utf-8 -*-
"""
执行任务的插件：
这个插件的主要职责是，去执行core_task的任务
"""
from django.db import models

from .base import Plugin


class DoCodeTaskPlugin(Plugin):
    """
    执行核心任务的插件
    """
    code = "do_core_task_plugin"
    name = "执行核心任务插件"

    class Meta:
        verbose_name = "执行任务插件"
        verbose_name_plural = verbose_name
