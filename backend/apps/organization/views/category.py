# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

from organization.models.team import Category
from organization.serializers.category import (
    CategoryModelSerializer,
    CategoryDetailModelSerializer
)
from modellog.mixins import LoggingViewSetMixin


class CategoryCreateApiView(LoggingViewSetMixin, generics.CreateAPIView):
    """
    Category Create Api View
    """
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (DjangoModelPermissions,)


class CategoryListApiView(generics.ListAPIView):
    """
    分类列表Api
    """
    queryset = Category.objects.filter(is_deleted=False).order_by("level")
    serializer_class = CategoryDetailModelSerializer
    permission_classes = (IsAuthenticated,)


class CategoryAllListApiView(LoggingViewSetMixin, generics.ListAPIView):
    """
    分类 All 列表Api
    """
    queryset = Category.objects.filter(is_deleted=False).order_by("level")
    serializer_class = CategoryDetailModelSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    分类详情 api View
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailModelSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly)

    def get_object(self):
        instance = super().get_object()
        return instance

    def update(self, request, *args, **kwargs):
        self.serializer_class = CategoryModelSerializer
        return super().update(request=request, *args, **kwargs)
