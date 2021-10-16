# -*- coding:utf-8 -*-
"""
流程
流程由多个Step组合而成
"""
from django.db import models
from django.contrib.auth import get_user_model

from codelieche.models import BaseModel

User = get_user_model()


class Flow(BaseModel):
    """
    流程中心的流程
    """
    delete_tasks = ("delete_task_change_code",)

    code = models.SlugField(verbose_name="流程的Code", blank=True, unique=True, max_length=108)
    name = models.CharField(verbose_name="流程", blank=True, max_length=128, null=True)
    user_id = models.IntegerField(verbose_name="创建者", blank=True, null=True)

    @property
    def user(self):
        if self.user_id:
            return self.get_relative_object_by_model(model=User, value=self.user_id)
        else:
            return None

    def delete_task_change_code(self):
        self.code = "{}_del_{}".format(self.code, self.strftime())
        self.save()

    @property
    def steps(self):
        # return self.step_set.filter(deleted=False).order_by("order")
        # 检索参数
        args = {
            "flow_id": self.id,
            "deleted": False,
        }
        # 获取相关的步骤
        return self.get_relative_object_by_content_type(
            app_label="workflow", model="step", args=args, many=True,
        )

    class Meta:
        verbose_name = "流程"
        verbose_name_plural = verbose_name

