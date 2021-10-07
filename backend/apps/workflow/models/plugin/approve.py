# -*- coding:utf-8 -*-
"""
审批插件：核心插件之一
"""
from django.db import models

from account.models import User
from .base import Plugin


class ApprovePlugin(Plugin):
    """
    审批插件
    """
    code = "approve_plugin"
    name = "审批插件"

    users = models.ManyToManyField(verbose_name="可审批的用户", to=User, related_name="can_approve_users", blank=True)
    user = models.ForeignKey(verbose_name="审批用户", to=User, on_delete=models.SET_NULL,
                             related_name="approved_user", blank=True, null=True)
    # 状态：cancel, error, success

    class Meta:
        verbose_name = "审批插件"
        verbose_name_plural = verbose_name
