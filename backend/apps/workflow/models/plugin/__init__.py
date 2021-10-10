# -*- coding:utf-8 -*-
from .base import Plugin
from .mysql import MySQLPlugin
from .project import ProjectCreatePlugin
from .shell import ShellExecutePlugin
from .approve import ApprovePlugin
from .do import DoCoreTaskPlugin
from .message import MessagePlugin
from .gitflow import GitFlowPlugin
from .jenkins import JenkinsPlugin


# 插件列表
plugins = [
    MySQLPlugin, ProjectCreatePlugin, ShellExecutePlugin, ApprovePlugin, DoCoreTaskPlugin, MessagePlugin,
    GitFlowPlugin, JenkinsPlugin,
]
plugins_list = []
plugins_dict = {}

for i in plugins:
    code = i.PLUGIN_INFO["code"]
    if issubclass(i, Plugin) and code and code not in plugins_dict:
        plugins_list.append(i)
        plugins_dict[code] = i
    else:
        raise ValueError("插件有误：{}".format(i))

