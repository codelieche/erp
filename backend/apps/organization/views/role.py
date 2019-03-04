# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

from organization.models.team import Role
from organization.serializers.role import (
    RoleModelSerializer,
    RoleDetailModelSerializer
)
from modellog.mixins import LoggingViewSetMixin


class RoleCreateApiView(LoggingViewSetMixin, generics.CreateAPIView):
    """
    Role Create Api View
    """
    queryset = Role.objects.all()
    serializer_class = RoleModelSerializer
    permission_classes = (DjangoModelPermissions,)


class RoleListApiView(generics.ListAPIView):
    """
    分类列表Api
    """
    queryset = Role.objects.filter(is_deleted=False).order_by("level")
    serializer_class = RoleDetailModelSerializer
    permission_classes = (IsAuthenticated,)


class RoleAllListApiView(LoggingViewSetMixin, generics.ListAPIView):
    """
    分类 All 列表Api
    """
    queryset = Role.objects.filter(is_deleted=False).order_by("level")
    serializer_class = RoleDetailModelSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)


class RoleDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    分类详情 api View
    """
    queryset = Role.objects.all()
    serializer_class = RoleDetailModelSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly)

    def get_object(self):
        instance = super().get_object()
        return instance

    def update(self, request, *args, **kwargs):
        self.serializer_class = RoleModelSerializer
        return super().update(request=request, *args, **kwargs)
