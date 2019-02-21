# -*- coding:utf-8 -*-
"""
一些工具视图
"""

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated


class CheckUserPermissionApiView(APIView):
    """
    检查当前用户的权限
    """
    # authentication_classes = (IsAuthenticated,)

    def post(self, request):
        # 1. get data
        user = request.user
        permission = request.data.get("permission", None)
        if not permission:
            content = {"status": False, "result": False, "message": "请传入permission"}
            return Response(data=content, status=400, content_type="application/json")

        if user.is_anonymous:
            content = {"status": False, "result": False, "message": "请登录"}
            return Response(data=content, status=401, content_type="application/json")

        # 2. check permission
        # u.has_perm("project.add_service")
        result = user.has_perm(permission)
        content = {
            "status": True,
            "result": result,
            "message": "检查{}的{}权限为{}".format(user.username, permission, result)
        }

        # 3. return response
        return Response(data=content, status=200, content_type="application/json")
