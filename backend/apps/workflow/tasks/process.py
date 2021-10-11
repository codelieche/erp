# -*- coding:utf-8 -*-
from celery import shared_task

from workflow.models.process import Process


@shared_task
def do_process_entry_task(process):
    # 直接执行entry_task
    process.entry_task()


@shared_task
def do_process_core_task(process: Process):
    # 直接执行entry_task
    results = process.core_task()
    success, result, output = results
    print("{}执行核心任务返回结果：{},{},{}".format(process, success, result, output))
