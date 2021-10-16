# -*- coding:utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from plugin.models import plugins_list


class PluginsListApi(APIView):
    """
    插件列表
    """

    def get(self, request):
        content = []
        for plugin in plugins_list:
            item = {
                "code": plugin.PLUGIN_INFO['code'],
                "name": plugin.PLUGIN_INFO['name'],
                "description": plugin.PLUGIN_INFO['description'],
            }
            content.append(item)
        return Response(data=content)
