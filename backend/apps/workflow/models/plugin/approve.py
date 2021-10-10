# -*- coding:utf-8 -*-
"""
审批插件：核心插件之一
"""
from django.db import models

from account.models import User
from workflow.models.workflow import WorkFlow
from .base import Plugin


class ApprovePlugin(Plugin):
    """
    审批插件
    """
    PLUGIN_INFO = {
        "code": "approve_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "审批插件",
        "description": "审批相关的插件"
    }

    users = models.ManyToManyField(verbose_name="可审批的用户", to=User, related_name="can_approve_users")
    user = models.ForeignKey(verbose_name="审批用户", to=User, on_delete=models.SET_NULL,
                             related_name="approved_user", blank=True, null=True)
    content = models.CharField(verbose_name="审批内容", blank=True, null=True, max_length=256)

    def entry_task(self, workflow, process, step):
        print("现在开始提醒用户，当前流程需要你审批咯")

    def execute_core_task(self):
        print("模拟执行核心任务")
        return True, "执行结果"

    # 状态：cancel, error, success
    def core_task(self, workflow: WorkFlow, process, step):
        if self.core_task_executed:
            # 这里考虑是返回True，暂时让只要重复触发核心任务就报错
            return False, "核心任务已经执行过了，不可继续执行"

        if process.status in ["agree", "success"]:
            if self.status not in ['todo']:
                return False, "当前插件不是todo不可执行核心任务:{}-{}-{}".format(workflow.id, process.id, self.id)
            else:
                # 把状态设置为doing，这样可防止重复执行
                self.status = "doing"
                self.save(update_fields=["status"])
                # 模拟执行核心任务，如果任务出错就把整个流程设置为错误，成功的话就把插件的状态改成agree/success
                success, result = self.execute_core_task()
                self.core_task_executed = True
                if success:
                    self.status = process.status
                    self.save()
                    # 这里考虑是否需要把process的状态改成success，但是暂时觉得没必要
                    # 进入下一个步骤
                    process.entry_next_process()
                    return True, "执行成功"
                else:
                    # 执行出错咯，大兄弟
                    self.status = "error"
                    self.save()
                    # Process保存错误状态
                    process.status = "error"
                    process.save()
                    # 流程保存错误状态
                    workflow.status = "error"
                    workflow.save()
                    # 执行出错了
                    return False, "执行出错：{}".format(result)
        else:
            return False, "Process未知状态({})，不可执行".format(process.status)

    class Meta:
        verbose_name = "审批插件"
        verbose_name_plural = verbose_name
