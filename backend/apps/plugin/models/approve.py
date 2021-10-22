# -*- coding:utf-8 -*-
"""
审批插件：核心插件之一
约定：审批插件，在配置step的时候，需要保存一个source到step的data中
这样审批插件的用户从source中来获取
"""
from django.db import models
from django.utils import timezone

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

    users = models.JSONField(verbose_name="可审批的用户")
    user = models.CharField(verbose_name="审批用户", max_length=128, blank=True, null=True)
    content = models.CharField(verbose_name="审批内容", blank=True, null=True, max_length=256)

    def entry_task(self, work, process, step):
        # 我需要有自己的entry_task，不可以自动跳入下一个步骤
        print("现在开始提醒用户，当前流程需要你审批咯:{}-{}".format(work, process))

        # 1. 获取到users的数据，这里面的数据是id或者邮箱的列表
        if not (isinstance(self.users, list) and len(self.users) > 0):
            # 直接报错
            result = "审批用户未配置，不可审批"
            # 记录过程的结果
            process.save_result(success=False, content=result)
            return process.handle_execute_result(success=False, result=result, output=None)
        else:
            title = "流程审批"
            content = f"【流程】\t{work.flow.name}\n【标题】\t{work.title}" \
                      f"\n【步骤】\t{step.name}\n【用户】\t{work.user}\n" \
                      f"【时间】\t{work.fmt_time_to_beijing(work.time_added)}\n" \
                      f"\n需要您审批!"

            # send_email(to=self.users, title=title, content=content)
            print(self.users, title, content)

    def execute_core_task(self, work=None):
        print("模拟执行审批核心任务：{}".format(self.id))
        return True, "执行结果", None

    # 状态：cancel, error, success
    def core_task(self, work, process, step, *args, **kwargs):
        if self.core_task_executed:
            # 这里考虑是返回True，暂时让只要重复触发核心任务就报错
            return False, "核心任务已经执行过了，不可继续执行", None

        if process.status in ["agree", "success"]:
            if self.status not in ['todo']:
                return False, "当前插件不是todo不可执行核心任务:{}-{}-{}".format(work.id, process.id, self.id), None
            else:
                # 把状态设置为doing，这样可防止重复执行
                self.status = "doing"
                # 保存用户
                user = kwargs.get('user')
                if user and hasattr(user, "username"):
                    self.user = user.username

                self.save(update_fields=["status", "user"])
                # 模拟执行核心任务，如果任务出错就把整个流程设置为错误，成功的话就把插件的状态改成agree/success
                success, result, output = self.execute_core_task()
                self.core_task_executed = True
                # 设置执行时间
                now = timezone.datetime.now(tz=timezone.utc)
                self.time_executed = now
                process.time_executed = now
                process.save()

                if success:
                    self.status = process.status
                    self.save()
                    # 这里考虑是否需要把process的状态改成success，但是暂时觉得没必要
                    # 进入下一个步骤
                    process.entry_next_process(prev_output=output)
                    return True, "执行成功", output
                else:
                    # 执行出错咯，大兄弟
                    self.status = "error"
                    self.save()
                    # Process保存错误状态
                    process.status = "error"
                    process.save()
                    # 流程保存错误状态
                    work.status = "error"
                    work.save()
                    # 执行出错了
                    return False, "执行出错：{}".format(result), output
        else:
            return False, "Process未知状态({})，不可执行".format(process.status), None

    class Meta:
        verbose_name = "审批插件"
        verbose_name_plural = verbose_name
