# -*- coding:utf-8 -*-
"""
具体的流程实例
"""
import json
import datetime

from django.db import models
from django.utils import timezone

from codelieche.models import BaseModel
from account.models import User
from workflow.models.flow import Flow
from workflow.models.step import Step


class Work(BaseModel):
    """
    工作流程，具体的每一条流程实例
    后续随着数据的增加，可实现分库分表，每类flow，放一张表中,work_flow_[code]的表
    这样的话code确定了之后就不可修改了
    """
    STATUS_CHOICES = (
        ("todo", "Todo"),
        ("doing", "进行中"),
        ("success", "成功"),
        ("error", "出错"),
        ("refuse", "拒绝"),
        ("cancel", "取消"),
        ("delete", "删除"),
        ("deliver", "转交"),
        ("agree", "通过"),
        ("done", "完成"),
    )
    # 根据不同的状态，重新保存一下status_code
    STATUS_CODE_DICT = {
        "todo": 1,
        "doing": 5,
        "success": 15,
        "error": 30,   # 出错、拒绝、成功、完成应该是一个级别的
        "refuse": 30,
        "cancel": 50,
        "delete": 50,
        "deliver": 15,
        "agree": 15,
        "done": 30,
    }
    delete_tasks = ['delete_task_change_status', 'delete_task_delete_process_logs']

    flow_id = models.IntegerField(verbose_name="流程")
    # 标题是必填的
    title = models.CharField(verbose_name="流程标题", max_length=256)
    user_id = models.IntegerField(verbose_name="创建者", blank=True, null=True)
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)
    status_code = models.SmallIntegerField(verbose_name="状态码", blank=True, default=0)
    current = models.IntegerField(verbose_name="当前步骤", blank=True, null=True)
    # 当前流程的数据，后续插件都会来这里取数据：step_id: {}  集合 step.data 组合实例化Plugin
    data = models.JSONField(verbose_name="流程数据", blank=True, null=True)
    # 结束时间
    time_finished = models.DateTimeField(verbose_name="完成时间", blank=True, null=True)

    @property
    def user(self):
        # 创建的时候user_id是记录用户的id的
        return self.get_relative_object_by_model(
            model=User, field="pk", value=self.user_id
        )

    @property
    def flow(self):
        if not self.flow_id:
            return None
        else:
            return self.get_relative_object_by_model(model=Flow, value=self.flow_id)

    def delete_task_change_status(self):
        # 删除的时候修改状态为delete
        self.status = "delete"
        self.save()

    @property
    def process_set(self):
        args = {
            "work_id": self.id,
            "deleted": False
        }
        return self.get_relative_object_by_content_type(
            app_label="workflow", model="process", args=args, many=True)

    @property
    def log_set(self):
        args = {
            "work_id": self.id,
            "deleted": False
        }
        return self.get_relative_object_by_content_type(
            app_label="workflow", model="worklog", args=args, many=True)

    def delete_task_delete_process_logs(self):
        for process in self.process_set:
            process.delete()
        for log in self.log_set:
            log.delete()

    def get_next_step(self, current=None):
        """
        获取下一个步骤，当current为None的时候就是取第一个
        :param current:
        :return:
        """
        if not current:
            return self.flow.steps.first()
        else:
            # 获取当前步骤的下一个，默认order是不相等的，且都是正确排好序的
            # next_step = self.flow.step_set.filter(order__gt=current.order, deleted=False).order_by("order").first()
            next_step = Step.objects.filter(
                flow_id=self.flow_id, order__gt=current.order, deleted=False).order_by("order").first()
            return next_step

    @staticmethod
    def get_plugin_data(step, data):
        """
        获取插件的数据
        :param step: 其实是Step的对象
        :param data: 是一个json对象
        :return:
        """
        # 2-2：取出初始化插件的数据
        # 2-2-1：先准备个dict
        plugin_data = {}

        # 2-2-2：从step配置的数据中获取
        if step.data:
            if isinstance(step.data, str):
                try:
                    step_plugin_data = json.loads(step.data)
                    plugin_data.update(step_plugin_data)
                except Exception as e:
                    msg = "步骤(id:{})配置的初始化数据有误".format(step.id)
                    return False, msg
            elif isinstance(step.data, dict):
                plugin_data.update(step.data)
        # 2-2-3：从传递的data中获取
        step_data_key = "step_{}".format(step.id)
        step_data = data.get(step_data_key)
        if step_data:
            if isinstance(step_data, str):
                try:
                    step_plugin_data = json.loads(step.data)
                    plugin_data.update(step_plugin_data)
                except Exception as e:
                    msg = "步骤(id:{})配置的初始化数据有误".format(step_data_key)
                    return False, msg
            elif isinstance(step_data, dict):
                plugin_data.update(step_data)

        # 返回插件数据
        return True, plugin_data

    @property
    def current_process(self):
        # 当前的process对象
        if self.current:
            return self.get_relative_object_by_content_type(
                app_label="workflow", model="process", value=self.current
            )
        else:
            return None

    @staticmethod
    def fmt_time_to_beijing(time, hours=8):
        try:
            value = time + datetime.timedelta(hours=hours)
            return value.strftime("%F %T")
        except Exception as e:
            return None

    def send_message(self, category="info", content="", process=None, step=None):
        """发送消息"""
        receives = [self.user_id]  # 接收用户

        if category == "done":
            # 发送完成消息: 发送提醒邮件
            title = "流程完成"
            content = f"【流程】\t{self.flow.name}\n【标题】\t{self.title}" \
                      f"\n【用户】\t{self.user.username}\n" \
                      f"【开始时间】\t{self.fmt_time_to_beijing(self.time_added)}\n" \
                      f"【完成时间】\t{self.fmt_time_to_beijing(self.time_finished)}\n" \
                      f"\n已经完成!"
        # 拒绝消息
        elif category == "refuse":
            # 发送错误消息: 发送提醒邮件
            title = "流程被拒绝"
            content = f"【流程】\t{self.flow.name}\n【标题】\t{self.title}" \
                      f"\n【用户】\t{self.user.username}\n" \
                      f"【时间】\t{self.fmt_time_to_beijing(self.time_added)}\n" \
                      f"\n\n\t{content}\n"

        # 错误消息
        elif category == "error":
            # 发送错误消息: 发送提醒邮件
            title = "流程出错"
            content = f"【流程】\t{self.flow.name}\n【标题】\t{self.title}" \
                      f"\n【用户】\t{self.user.username}\n" \
                      f"【开始时间】\t{self.fmt_time_to_beijing(self.time_added)}\n" \
                      f"【出错时间】\t{self.fmt_time_to_beijing(self.time_finished)}\n" \
                      f"\n执行出错!\n\n{content}"
            # work.user，保存的是u_id

        # 执行发送消息
        # send_email(to=receives, title=title, content=content)
        print(receives, title, content, "send email")

    @property
    def steps_count(self):
        args = {
            "flow_id": self.flow_id,
            "deleted": False,
        }
        count = self.get_relative_object_by_model(Step, args=args, many=True).count()
        return count

    @property
    def process_count(self):
        args = {
            "flow_id": self.flow_id,
            "work_id": self.id,
        }
        count = self.get_relative_object_by_content_type(
            app_label="workflow", model="process", args=args, many=True).count()
        return count

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 校验status
        if not self.status:
            self.status = "todo"

        # 设置status_code
        if self.status_code != self.STATUS_CODE_DICT[self.status]:
            self.status_code = self.STATUS_CODE_DICT[self.status]

        # 如果状态是：cancel、delete、done就需要设置一下结束时间
        if self.status in ["error", "cancel", "delete", "done"]:
            self.time_finished = timezone.datetime.now()
            # 设置完成
            # if self.status == "done":
            #     content = "流程完成"
            #     category = "done"
            #     WorkLog.objects.create(work_id=self.id, category=category, content=content)

        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)

    class Meta:
        verbose_name = "流程实例"
        verbose_name_plural = verbose_name
        ordering = ("status_code", "-id")
