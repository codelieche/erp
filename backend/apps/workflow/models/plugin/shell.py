# -*- coding:utf-8 -*-
"""
执行Shell命令的插件
"""
from django.db import models

from .base import Plugin


class ShellExecutePlugin(Plugin):
    """
    执行Shell命令的插件
    """

    code = "shell_execute"
    name = "执行Shell命令插件"

    class Meta:
        verbose_name = "执行Shell命令插件"
        verbose_name_plural = verbose_name
