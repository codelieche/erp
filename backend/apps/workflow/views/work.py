# -*- coding:utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response

from codelieche.views.viewset import ModelViewSet
from workflow.models.work import Work
from workflow.models.process import Process
from workflow.models.log import WorkLog
from workflow.serializers.work import WorkModelSerializer, WorkInfoModelSerializer
from workflow.tasks.process import do_process_core_task


class WorkApiModelViewSet(ModelViewSet):
    """
    Work Flow Api View Set
    """
    queryset = Work.objects.filter(deleted=False)
    serializer_class_set = (WorkModelSerializer, WorkInfoModelSerializer)

    @action(methods=["POST"], detail=False, description="执行当前步骤的操作")
    def action(self, request):
        # 1. 获取当前的相关数据
        # 1-1. 获取到流程实例对象
        work_id = request.data.get('work')
        if not work_id:
            content = {
                "status": False,
                "message": "未传入work"
            }
            return Response(data=content, status=400)
        work = Work.objects.filter(id=work_id, deleted=False).first()

        if not work:
            content = {
                "status": False,
                "message": "传入的work不存在"
            }
            return Response(data=content, status=400)

        # 1-2：获取process
        # 1-2-1：获取到process的it，如果不是int那后面是会报错的
        process_id = request.data.get('process')
        if not process_id:
            content = {
                "status": False,
                "message": "未传入process"
            }
            return Response(data=content, status=400)
        # 1-2-2：根据id得到流程对象
        process = Process.objects.filter(id=process_id, work_id=work.id).first()
        if not process:
            content = {
                "status": False,
                "message": "传入的process不存在"
            }
            return Response(data=content, status=400)
        # 1-2-3：校验process是否正确
        # 判断当前流程实例的当前process是否是这个
        if work.current != process.id:
            content = {
                "status": False,
                "message": "当前流程已经变更"
            }
            return Response(data=content, status=400)
        # 如果process的状态不是todo也是不可操作的
        if process.status not in ["todo", "doing"]:
            content = {
                "status": False,
                "message": "当前流程Process的状态不是todo/doing，不可操作"
            }
            return Response(data=content, status=400)

        # 1-3：获取到状态
        status = request.data.get("status")
        if status not in Work.STATUS_CODE_DICT:
            content = {
                "status": False,
                "message": "传入的status({})无效".format(status)
            }
            return Response(data=content, status=400)

        # 2. 根据状态执行相关的操作
        # 状态应该是：cancel/refuse/agree/sucess， doing/error/done的状态应该由异步任务去设置的
        # 2-1：如果是取消/拒绝，就直接跳过
        user = request.user
        if status in ["cancel", "refuse"]:
            process.status = status
            process.save()
            # 保存一下当前这个插件的执行状态
            process.plugin_obj.status = status
            process.plugin_obj.save()
            # 流程实例的状态，设置为取消/拒绝
            work.status = status
            work.save()
            # 记录日志
            if status == "cancel":
                content = "{}取消了步骤({})".format(user.username, process.name)
            else:
                content = "{}拒绝了步骤({})".format(user.username, process.name)
            WorkLog.objects.create(work_id=work.id, user=user, category="error", content=content)

            # 返回取消/拒绝成功的消息
            content = {
                "status": True,
                "message": "操作成功"
            }
            return Response(data=content)

        # 2-2: 如果是：agree、success就表示可以执行当前的process的核心任务了
        if status in ["agree", "success"]:
            process.status = status
            process.save()
            print("执行当前process的核心任务：", work, process)

            # 记录日志
            content = "{}通过了步骤({})".format(user.username, process.name)
            WorkLog.objects.create(work_id=work.id, user=user, category="success", content=content)

            # 执行过程的核心任务
            success, result, output = process.core_task(user=user)
            print("{}执行核心任务返回结果：".format(process), success, result, output)

            # 异步执行
            # do_process_core_task.delay(process)

            # 操作成功
            content = {
                "status": True,
                "message": "操作成功"
            }
            # 操作成功
            return Response(data=content)

        content = {
            "status": False,
            "message": "未知状态，数据传递有误成功"
        }
        return Response(data=content, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 如果当前流程已经完成了就不可删除了
        if instance.status in ["success"]:
            content = {
                "status": False,
                "message": "当前流程已经执行完成了，不可删除"
            }
            return Response(data=content, status=400)
        else:
            # 删除流程
            user = request.user.username
            # 设置完成
            content = "删除流程"
            category = "error"
            WorkLog.objects.create(work_id=instance.id, user=user, category=category, content=content)
            return super().destroy(request, *args, **kwargs)
