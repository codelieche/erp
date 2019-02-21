# -*- coding:utf-8 -*-
"""
CSRF中间件
"""
from django.utils.deprecation import MiddlewareMixin


class ApiDisableCSRF(MiddlewareMixin):
    """
    API的请求取消CSRF校验
    """

    def is_api_request(self, request):
        """
        判断是否是api的请求
        :param request: 请求对象
        :return: True or False
        """
        path = request.path.lower()
        return path.startswith("/api/")

    def process_request(self, request):
        if self.is_api_request(request):
            # 给request设置属性，不要检查csrf token
            setattr(request, "_dont_enforce_csrf_checks", True)
