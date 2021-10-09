# -*- coding:utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response

from codelieche.views.viewset import ModelViewSet
from workflow.models.workflow import WorkFlow
from workflow.models.process import Process
from workflow.serializers.workflow import WorkFlowModelSerializer, WorkflowInfoModelSerializer


class WorkFlowApiModelViewSet(ModelViewSet):
    """
    Work Flow Api View Set
    """
    queryset = WorkFlow.objects.filter(deleted=False)
    serializer_class_set = (WorkFlowModelSerializer, WorkflowInfoModelSerializer)

    @action(methods=["POST"], detail=True, description="执行当前步骤的操作")
    def action(self, request, pk=None):
        # 1. 获取当前的相关数据
        # 1-1. 获取到流程实例对象
        workflow = self.get_object()

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
        process = Process.objects.filter(id=process_id, workflow_id=pk).first()
        if not process:
            content = {
                "status": False,
                "message": "传入的process不存在"
            }
            return Response(data=content, status=400)
        # 1-2-3：校验process是否正确
        # 判断当前流程实例的当前process是否是这个
        if workflow.current != process.id:
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
        if status not in WorkFlow.STATUS_CODE_DICT:
            content = {
                "status": False,
                "message": "传入的status({})无效".format(status)
            }
            return Response(data=content, status=400)

        # 2. 根据状态执行相关的操作
        # 状态应该是：cancel/refuse/agree/sucess， doing/error/done的状态应该由异步任务去设置的
        # 2-1：如果是取消/拒绝，就直接跳过
        if status in ["cancel", "refuse"]:
            process.status = status
            process.save()
            # 保存一下当前这个插件的执行状态
            process.plugin_obj.status = status
            process.plugin_obj.save()
            # 流程实例的状态，设置为取消/拒绝
            workflow.status = status
            workflow.save()
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
            print("执行当前process的核心任务")
            process.core_task()

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
            return super().destroy(request, *args, **kwargs)
