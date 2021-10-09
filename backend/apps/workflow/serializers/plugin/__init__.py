# -*- coding:utf-8 -*-

from .approve import ApprovePluginModelSerializer
from .do import DoCoreTaskPluginModelSerializer
from .message import MessagePluginPluginModelSerializer
from .mysql import MySQLPluginPluginModelSerializer
from .project import ProjectCreatePluginModelSerializer
from .shell import ShellExecutePluginModelSerializer

plugin_serailizers = [
    ApprovePluginModelSerializer, DoCoreTaskPluginModelSerializer,
    MessagePluginPluginModelSerializer, MySQLPluginPluginModelSerializer,
    ProjectCreatePluginModelSerializer, ShellExecutePluginModelSerializer
]

# 校验插件的时候需要用到的序列化
plugin_serializers_mapping = {}
for item in plugin_serailizers:
    code = item.Meta.model.PLUGIN_INFO['code']
    if code and code not in plugin_serializers_mapping:
        plugin_serializers_mapping[code] = item