# -*- coding:utf-8 -*-
"""
项目流程相关的插件
项目插件，主要是创建项目，然后填写相关的参数
"""

from django.db import models

from .base import Plugin


class ProjectCreatePlugin(Plugin):
    """
    项目创建的插件
    """
    code = "project_create"
    name = "项目创建插件"

    class Meta:
        verbose_name = "项目创建"
        verbose_name_plural = verbose_name
