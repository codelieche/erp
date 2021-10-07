# -*- coding:utf-8 -*-
"""
执行MySQL的插件
"""
from django.db import models

from .base import Plugin


class MySQLPlugin(Plugin):
    """
    MySQL相关的插件
    主要是执行SQL的插件
    """
    code = "mysql_plugin"
    name = "MySQL插件"

    class Meta:
        verbose_name = "MySQL插件"
        verbose_name_plural = verbose_name
