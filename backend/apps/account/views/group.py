# -*- coding:utf-8 -*-
"""
账号分组相关的视图函数
"""
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

from codelieche.views.viewset import ModelViewSet
from account.serializers.group import GroupModelSerializer, GroupInfoSerializer


class GroupApiModelViewSet(ModelViewSet):
    """
    分组相关API
    """
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    serializer_class_set = (GroupModelSerializer, GroupInfoSerializer)
    permission_classes = (IsAuthenticated,)
    search_fields = ('name',)
    filter_fields = ("name",)
    ordering_fields = ("id",)
    ordering = ("id",)
