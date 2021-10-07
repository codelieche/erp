# -*- coding:utf-8 -*-
"""
发送消息的插件
"""
from django.db import models

from .base import Plugin


class MessagePlugin(Plugin):
    """
    发送消息的插件
    """
    code = "message_plugin"
    name = "消息插件"

    class Meta:
        verbose_name = "消息插件"
        verbose_name_plural = verbose_name
