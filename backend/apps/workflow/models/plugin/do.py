# -*- coding:utf-8 -*-
"""
执行任务的插件：
这个插件的主要职责是，去执行core_task的任务
"""
from django.db import models

from .base import Plugin
from workflow.models.workflow import WorkFlow


class DoCoreTaskPlugin(Plugin):
    """
    执行核心任务的插件
    """
    PLUGIN_INFO = {
        "code": "do_core_task_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "执行核心任务插件",
        "description": "执行核心任务的插件"
    }
    # 能执行核心任务的process状态，一般都是agree和sucess即可
    CAN_EXECUTE_CORE_TASK_STATUS = ["agree", "success"]

    # 执行任务可以是自动执行也可以是手动执行
    auto_execute = models.BooleanField(verbose_name="自动执行", blank=True, default=False)

    def entry_task(self, workflow, process, step):
        print("进入do_core_task流程，如果是自动执行的，那么我们就执行核心任务")
        # process.entry_next_process()
        if self.auto_execute:
            self.core_task(workflow=workflow, process=process, step=step)

    def core_task(self, workflow: WorkFlow, process, step):
        # 统一在proces中就判断一下是否已经执行了，这里就无需判断了
        # if self.core_task_executed:
        #     # 这里考虑是返回True，暂时让只要重复触发核心任务就报错
        #     return False, "核心任务已经执行过了，不可继续执行"

        if self.status not in ['todo', "agree", "sucess"]:
            return False, "当前插件不是todo不可执行核心任务:{}-{}-{}".format(workflow.id, process.id, self.id)
        else:
            # 把状态设置为doing，这样可防止重复执行
            self.status = "doing"
            self.save()

        # 获取Flow的所有步骤，由后向前执行其核心任务，每个插件有个核心任务的开关，执行完的就无需执行，未执行的就执行一下
        # 遍历当前流程所有的process，执行其核心task
        process_list = workflow.process_set.filter(deleted=False).order_by("-id")
        for process_i in process_list:
            # 跳过当前流程
            if process_i == process:
                continue
            print("检查当前process是否需要执行核心任务：", process_i)

            if process_i.status in ["todo", "agree", "success"]:
                if process_i.plugin_obj.core_task_executed:
                    continue
                else:
                    # 执行当前process的核心任务
                    sucess, result = process_i.core_task()
                    if not sucess:
                        # 执行出错了：
                        msg = "执行Process:{}, 出错:{}".format(process_i, result)
                        print(msg)
                        # 设置错误状态
                        # 设置当前插件的状态为False
                        self.status = "error"
                        self.save()
                        # 设置流程的状态为失败
                        workflow.status = "error"
                        workflow.save()
                        return False, msg
            else:
                continue
        # 如果执行到这里，那么就是插件成功执行了，修改状态
        self.status = "success"
        self.save()
        # 这里比较特殊，还需要修改process的状态为成功
        process.status = "success"
        process.save()
        # 进入流程的下一个步骤
        process.entry_next_process()

        print("执行workfow.doCoreTask{}的核心任务成功".format(workflow))
        return True, "执行成功"

    class Meta:
        verbose_name = "执行任务插件"
        verbose_name_plural = verbose_name
