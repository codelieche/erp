# -*- coding:utf-8 -*-
"""
流程中心的步骤
"""
from django.db import models

from codelieche.models import BaseModel
from workflow.models.plugin import plugins_dict
from workflow.serializers.plugin import plugin_serializers_mapping
from workflow.models.flow import Flow


class Step(BaseModel):
    """
    流程的步骤
    """
    flow = models.ForeignKey(verbose_name="流程", to=Flow, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="步骤名称", max_length=128, blank=True, null=True)
    # 步骤有个阶段和排序，由小到大的排序
    stage = models.SmallIntegerField(verbose_name="阶段", blank=True, default=1)
    # 我们会根据一个算法来计算order，stage * 10**stage + step 来计算出在flow中的排序order
    step = models.SmallIntegerField(verbose_name="步骤", blank=True, default=1)
    order = models.IntegerField(verbose_name="排序", blank=True, default=1)
    plugin = models.CharField(verbose_name="插件的code", max_length=64)
    data = models.JSONField(verbose_name="插件初始化数据", blank=True, null=True)
    # 当前步骤是否自动立刻执行: 最终是很多步骤会一步一步的去执行
    auto_execute = models.BooleanField(verbose_name="自动执行", blank=True, default=False)

    @property
    def plugin_class(self):
        # 如果插件不存在就直接报错
        return plugins_dict[self.plugin]

    @property
    def plugin_serializer_class(self):
        # 如果插件的序列化类不存在，也直接报错
        return plugin_serializers_mapping[self.plugin]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # 1. 计算order
        # 1-1: 判断stage和step的值
        if not self.stage:
            self.stage = 1
        if not self.step:
            self.step = 1
        # 1-2：计算order，这个是为了flow整体的排序
        self.order = 10 ** self.stage + self.step

        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)

    class Meta:
        verbose_name = "流程步骤"
        verbose_name_plural = verbose_name
