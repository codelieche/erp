# -*- coding:utf-8 -*-
"""
作业流程的没一个过程
Flow配置的一个Step对应一个Process，可以转交的话，就对应多个了

process的设计：
1. entry_task: 进入这个过程
2. core_task: 核心任务
3. auto: 是否自动执行【里面有好一些规范，插件是需要遵守的，如果不遵守那就没办法了】
4. entry_next_process: 进入下一个步骤
5. 很多的设计都是要插件配合的，因为process一般是固定写好了 不会大动，但是plugin是会不断添加的
"""
from django.db import models

from codelieche.models import BaseModel
from plugin.models import plugins_dict
from plugin.serializers import plugin_serializers_mapping
from workflow.models.work import Work
from workflow.models.step import Step
from workflow.models.log import WorkLog
from workflow.models.result import ProcessResult


class Process(BaseModel):
    """
    流程中的过程
    """
    flow_id = models.IntegerField(verbose_name="流程", blank=True, null=True)
    work_id = models.IntegerField(verbose_name="流程实例")
    step_id = models.IntegerField(verbose_name="步骤")
    name = models.CharField(verbose_name="步骤名称", max_length=128)
    order = models.IntegerField(verbose_name="排序")  # 其实是步骤的排序
    # 我们先创建好Process，开始是没有设置plugin插件的, 当到达这一步之后就开始实例化插件
    # 实例化插件的时候还需要和传入的值结合一下
    plugin = models.CharField(verbose_name="插件", max_length=128)
    data = models.JSONField(verbose_name="插件数据")
    plugin_id = models.IntegerField(verbose_name="插件实例的ID", blank=True, null=True)
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)
    # 当前步骤是否自动执行的：如果是，那么插件会在entry_task的时候自动进入core_task
    auto = models.BooleanField(verbose_name="自动执行", blank=True, default=False)
    receive_input = models.BooleanField(verbose_name="是否接收输入", blank=True, default=False)
    # 执行时间
    time_executed = models.DateTimeField(verbose_name="执行时间", blank=True, null=True)

    @property
    def flow(self):
        if not self.flow_id:
            raise ValueError("未配置流程:Process ID: {}".format(self.id))
        else:
            return self.get_relative_object_by_content_type(
                app_label="workflow", model="flow", value=self.flow_id
            )

    @property
    def work(self):
        if not self.work_id:
            raise ValueError("未配置作业流程:Process ID: {}".format(self.id))
        else:
            return self.get_relative_object_by_model(model=Work, value=self.work_id)

    @property
    def step(self):
        if not self.step_id:
            raise ValueError("未配置步骤:Process ID: {}".format(self.id))
        else:
            return self.get_relative_object_by_model(model=Step, value=self.step_id)

    @property
    def result(self):
        try:
            result = self.get_relative_object_by_content_type(
                app_label="workflow", model="processresult", field="process_id", value=self.id, many=True).first()
            return result
        except Exception:
            # 有可能是还未设置结果呢
            return None

    def get_or_create_plugin(self, prev_output):
        # 如果已经有plugin_id了那么就返回插件
        plugin_class = plugins_dict[self.plugin]

        if self.plugin_id:
            # 1. 获取到插件类对象
            return plugin_class.objects.get(id=self.plugin_id)
        else:
            # 2. 创建插件
            # 2-1: 获取到相关数据
            plugin_serializer_class = plugin_serializers_mapping[self.plugin]
            plugin_data = self.data
            if not isinstance(plugin_data, dict):
                raise ValueError("Process的数据必须是dict类型")
            # 2-2: 判断传入的数据
            if self.receive_input and isinstance(prev_output, dict):
                prev_out_put_fields = {}
                for k in plugin_class.RECEIVE_INPUT_FIELDS:
                    if k in prev_output:
                        prev_out_put_fields[k] = prev_output[k]
                # 更新插件的数据
                plugin_data.update(prev_out_put_fields)

            # 2-3: 实例化插件
            serializer = plugin_serializer_class(data=plugin_data)
            if serializer.is_valid(raise_exception=True):
                plugin = serializer.save()
                # 记得保存一下插件的id
                self.plugin_id = plugin.id
                self.status = "todo"
                self.save()
                return plugin
            else:
                raise ValueError("{}".format(serializer.errors))

    @property
    def plugin_obj(self):
        # 1. 获取到当前的插件对象
        plugin_class = plugins_dict[self.plugin]
        # 如果传递的plugin不存在就直接报错
        plugin = plugin_class.objects.get(id=self.plugin_id)

        # 如果插件不存在，直接出错
        return plugin

    def receive_input_value(self, prev_output):
        # 接收上一步的输出值，更新当前插件的值
        updated = False
        plugin_obj = self.plugin_obj
        if prev_output and isinstance(prev_output, dict):
            for k in plugin_obj.RECEIVE_INPUT_FIELDS:
                if k in prev_output:
                    setattr(plugin_obj, k, prev_output[k])
                    if not updated:
                        updated = True
        # 如果更新了就需要保存一下
        if updated:
            plugin_obj.save()
        return self

    def entry_task(self, prev_output=None, *args, **kwargs):
        # 进入这个process，可能是发短信，也可能是立刻进入下一个环节
        # 其实是调用插件实例的事件
        print("进入当前过程，处理事件: Process:{}-{}".format(self.id, self.step.name))
        # 1. 获取到当前的插件对象
        # 如果传递的plugin不存在就直接报错
        plugin = self.get_or_create_plugin(prev_output=prev_output)

        # 2. 执行插件的entry任务
        # 当process.auto，就会再entry_task中自动进入core_task, 这算是个约定，插件需要这样遵循
        results = plugin.entry_task(work=self.work, process=self, step=self.step, *args, **kwargs)
        # 3. 有些插件是直接进入下一个任务的

        return results

    def entry_next_process(self, prev_output=None, *args, **kwargs):
        # 1. 获取实例化Plugin所需的数据
        # 1-1：下一个任务
        next_process = self.work.get_next_step(current=self)
        work = self.work

        # 修改一下状态
        if work.status == "todo":
            work.status = "doing"
            work.save()

        if not next_process:
            print(self, "没有下一个步骤了，无需执行， 开始设置整个流程的状态为Done")
            # 到这里应该是要检查一下work的状态了，比如全部修改成done
            work.status = "done"
            work.save()

            # 发送完成消息：发送提醒
            work.send_message(category="done")
            return

        # 1-2：实例化下一个插件的数据
        if not isinstance(next_process, Process):
            raise ValueError("work的下一步不是process对象")

        next_step_plugin = next_process.get_or_create_plugin(prev_output=prev_output)

        if next_step_plugin:
            work.current = next_process.id
            work.step_done += work.step_done  # 已经完成的步数需要+1
            work.save()

        # 这个还得待确定，暂时先修改
        # 在进入下一个process的下一个任务之前，如果当前process的状态为todo，那么需要设置为success
        if self.status == "todo":
            self.status = "success"
            self.save()

        # 触发进入这个流程的事件
        return next_process.entry_task(*args, **kwargs)  # 执行进入流程相关的事件

    def handle_execute_result(self, success=False, result=None, output=None):
        """
        当前过程设置了字段执行
        出错/成功都需要调用这个方法，会修改自己的状态，同时会修改work的状态
        :param success: 是否成功执行
        :param result: 出错的信息
        :param output: 输出的结果，可作为下一步的输入
        :return:
        """
        # 1. 校验process的状态
        if self.status in ["error", "cancel", "done"]:
            raise ValueError("出现这个错误，请调整代码逻辑:{}".format(result))

        # 2. 设置状态
        status = "success" if success else "error"
        self.status = status
        self.save()

        # work的状态，如果是出错我们就保存，是成功就交给下一步的操作来处理
        if not success:
            work = self.work  # 先获取work对象
            work.status = "error"
            work.save()
            work.send_message(category="error", content=result)

        # 3. 如果成功，那么就需要自动进入下一个步骤
        if success and self.auto:
            self.entry_next_process(prev_output=output)

    def core_task(self, *args, **kwargs):
        # 进入这个process的核心任务，可能是发短信，也可能是直接通过，进入下一个环节
        # 其实是调用插件实例的事件
        # print("进入当前过程，核心事件处理事件")
        # 1. 获取到当前的插件对象
        plugin = self.plugin_obj

        # 2. 执行插件的核心任务
        # 2-1：判断是否可以进入核心任务
        if self.status in plugin.CAN_EXECUTE_CORE_TASK_STATUS or (self.status == "todo" and self.auto):
            if plugin.core_task_executed:
                # print("当前插件的核心任务已经执行过了，不可执行")
                return False, "核心任务已经执行过了，不可继续执行", None
            else:
                # if plugin.status not in ["to-do"]:
                #     return False, "当前插件状态不是todo不可执行"
                # 执行插件的核心任务：非常重要哦
                results = plugin.core_task(work=self.work, process=self, step=self.step, *args, **kwargs)
                if len(results) == 2:
                    success, result = results
                    output = None
                elif len(results) == 3:
                    success, result, output = results
                else:
                    raise ValueError("插件{}执行核心任务返回的结果格式不正确".format(plugin))

                # 记录执行日志:
                if success:
                    content = "{}:执行成功".format(self.step.name)
                    category = "success"
                else:
                    content = "{}:执行失败:{}".format(self.step.name, result)
                    category = "error"
                WorkLog.objects.create(work_id=self.work_id, category=category, content=content)

                # 核心任务执行失败，应该终止和报错了
                # 考虑一下，这里是否需要修改process的状态
                return success, result, output

        else:
            msg = "Process:{},当前状态({})不可以执行插件的核心任务".format(self, self.status)
            print(msg)
            return False, msg, None

        # 3. 有些插件是直接进入下一个任务的

    def save_result(self, success=False, content=""):
        """
        保存结果: 注意我们一个Process只保存一次结果
        """
        result, created = ProcessResult.objects.get_or_create(process_id=self.id)
        result.success = success
        result.content = content
        result.save()
        return result

    class Meta:
        verbose_name = "过程"
        verbose_name_plural = verbose_name
