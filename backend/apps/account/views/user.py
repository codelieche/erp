# -*- coding:utf-8 -*-
"""
账号登陆登出相关api
"""
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsSuperUserOrReadOnly
from modellog.mixins import LoggingViewSetMixin
from account.serializers.user import (
    UserLoginSerializer,
    UserAllListSerializer,
    UserSimpleInfoSerializer,
    UserDetailSerializer,
    UserModelSerializer
)
from account.models import User

# 用户导航数据
from .nav_data import superuser_nav, normal_user_nav


class LoginView(APIView):
    """
    用户登陆api View
    1. GET: 判断用户是否登陆
    2. POST: 账号登陆
    """

    def get(self, request):
        # get判断当前客户端是否登陆
        # 如果登陆了返回{logined: true},未登录返回{logined: false}
        user = request.user
        if user.is_authenticated:
            content = {
                "logined": True,
                "username": user.username,
                # "is_superuser": user.is_superuser
            }
        else:
            content = {
                "logined": False
            }

        return JsonResponse(data=content)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username", "")
            password = serializer.validated_data.get("password", "")

            # 调用authenticate方法：注意settings.py中的AUTHTICATION_BACKENDS
            user = authenticate(username=username, password=password)

            if user is not None:
                # 登陆
                if user.is_active:
                    # 用户有个can_view的字段，如果是False就不可以登陆本系统
                    if user.can_view:
                        login(request, user)
                        content = {
                            "status": True,
                            "username": user.username,
                            "message": "登陆成功",
                        }
                    else:
                        content = {
                            "status": False,
                            "message": "您还没登录权限，请找管理员开通！"
                        }
                else:
                    content = {
                        "status": False,
                        "message": "用户({})已被禁用".format(user.username)
                    }
                return JsonResponse(data=content, status=status.HTTP_200_OK)
            else:
                content = {
                    "status": False,
                    "message": "账号或者密码不正确"
                }
                return JsonResponse(data=content, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def account_logout(request):
    """
    退出登陆
    :param request: http请求
    :return:
    """
    logout(request)
    # 有时候会传next
    next_url = request.GET.get("next", "/")
    return JsonResponse({"status": True, "next": next_url})


class UserCreateApiView(generics.CreateAPIView):
    """
    添加用户API
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserListView(generics.ListAPIView):
    """
    用户列表
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSimpleInfoSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)


class UserAllListView(generics.ListAPIView):
    """
    所有用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserAllListSerializer
    # 分页和权限
    pagination_class = None
    # 权限
    permission_classes = (IsAuthenticated, )


class UserTuiguanListView(generics.ListAPIView):
    """
    所有用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserAllListSerializer
    # 分页和权限
    pagination_class = None
    # 权限
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        request = self.request
        user = request.user

        queryset = User.objects.filter(parent=user)

        return queryset


class UserDetailView(LoggingViewSetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    用户详情api
    1. GET：获取用户详情
    2. PUT：修改用户信息
    3. DELETE：删除用户信息【需要自定义】
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # 权限控制
    permission_classes = (IsSuperUserOrReadOnly,)

    def delete(self, request, *args, **kwargs):
        # 第1步：获取到用户
        user = self.get_object()
        if user == request.user:
            content = {
                "message": "不可以删除自己"
            }
            return Response(content, status=400)

        # 第2步：对用户进行删除
        # 2-1：设置deleted和is_active
        user.is_deleted = True
        user.is_active = False
        user.save()

        # 第3步：返回响应
        response = Response(status=204)
        return response


class UserChangePasswordApiView(APIView):
    """
    用户修改密码
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        oldpassword = request.data.get("oldpassword")
        password = request.data.get("password")
        repassword = request.data.get("repassword")
        if oldpassword and password and repassword:
            # 判断密码：
            if not user.check_password(oldpassword):
                content = {"status": False, "message": "旧密码错误，请重试"}
                return JsonResponse(data=content, status=400)

            if len(password) < 8:
                content = {"status": False, "message": "新密码长度小于8"}
                return JsonResponse(data=content, status=400)

            if oldpassword == password:
                content = {"status": False, "message": "新的密码和旧的密码相同"}
                return JsonResponse(data=content, status=400)
            else:
                if password == repassword:
                    user.set_password(password)
                    user.save()
                    return JsonResponse({"status": True, "message": "密码修改成功"})
                else:
                    content = {"status": False, "message": "密码和确认密码不相同"}
                    return JsonResponse(data=content, status=400)
        else:
            content = {"status": False, "message": "密码不可为空"}
            return JsonResponse(data=content, status=400)


class UserNavApiView(APIView):
    """
    获取用户导航数据
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # 待优化
        user = request.user

        if user.is_superuser:
            return Response(superuser_nav, content_type='application/json')
        else:
            return Response(normal_user_nav, content_type='application/json')
