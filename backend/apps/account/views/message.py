# -*- coding:utf-8 -*-
"""
用户消息相关的视图
"""
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from codelieche.views.viewset import ModelViewSet
from account.serializers.message import MessageSerializer
from account.models import Message


class MessageApiModelViewSet(ModelViewSet):
    """
    Message Api View Set
    """
    queryset = Message.objects.filter(is_deleted=False)
    serializer_class = MessageSerializer
    serializer_class_set = (MessageSerializer,)
    # 权限控制
    permission_classes = (IsAuthenticated,)

    # 搜索和过滤
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('scope', 'unread')
    search_fields = ('title', 'content')
    ordering_fields = ('id', 'time_added')
    ordering = ('-time_added',)

    def get_queryset(self):
        # 第1步：获取到请求的用户
        # 用户只可以看到自己的消息列表
        user = self.request.user

        # 第2步：获取到type【read、unread、all】
        _type = self.request.GET.get('type', 'all')
        if _type == 'read':
            queryset = Message.objects.filter(user=user, is_deleted=False, unread=False) \
                .order_by('-id')
        elif _type == 'unread':
            queryset = Message.objects.filter(user=user, is_deleted=False, unread=True) \
                .order_by('-id')
        else:
            queryset = Message.objects.filter(user=user, is_deleted=False).order_by('-id')

        # 第3步：返回结果集
        return queryset

    def get_object(self):
        # 1. 先获取到用户
        user = self.request.user

        # 2. 调用父类的方法获取到这个对象
        instance = super().get_object()

        # 3. 如果这个对象user是请求的用户，那么返回对象，不是的话返回None
        if instance and user == instance.user:
            return instance
        else:
            return None

    def retrieve(self, request, *args, **kwargs):
        # 1. 获取到对象
        instance = self.get_object()

        # 2. 修改unread
        if instance.unread:
            instance.unread = False
            instance.save(update_fields=('unread',))
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # 1. 获取到user和对象
        user = self.request.user
        instance = self.get_object()

        # 2. 如果是自己的消息或者是超级管理员，那么就可以删除本条消息
        if instance.is_deleted:
            response = Response(status=204)
        else:
            if instance.user == user or user.is_superuser:
                instance.is_deleted = True
                instance.save()
                response = Response(status=204)
            else:
                response = Response("没权限删除", status=403)

        # 3. 返回响应
        return response
