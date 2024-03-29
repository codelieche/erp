"""
程序初始化程序
1. 创建初始化用户：kanban:changeme
2. 创建配置导航菜单：
3. 创建默认的文档分组：Group,且设置Owner为kanban
"""
import os

from rest_framework.views import APIView
from django.http.response import JsonResponse

from account.models import UserProfile
from config.models import Menu


def check_user_or_create_superuser():
    """
    检查是否有用户，如果没有就创建个超级用户
    """
    # 1. 统计用户数
    if UserProfile.objects.count() == 0:
        # 2. 创建用户
        username = os.environ.get("DEFAULT_USER_NAME", "erp")
        user = UserProfile.objects.create(
            username=username, nick_name=username, mobile=username,
            can_view=True, is_superuser=True, is_staff=True
        )

        # 3. 设置密码
        password = os.environ.get("DEFAULT_USER_PASSWORD", "changeme")
        user.set_password(password)
        user.save()
        print("设置用户{}的密码为：{}".format(username, password))


def check_menu_or_create_menus():
    """
    检查是否有没有菜单，没有的话就创建
    """
    # 1. 统计菜单
    if Menu.objects.count() > 0:
        return
    
    # 2. 初始化的菜单
    menus = [
        {
            "order": 5,
            "title": "用户中心",
            "slug": "/user",
            "icon": "user-circle",
            "permission": "",
            "target": "_self",
            "is_link": False,
            "link": "",
            "is_deleted": False,
            "level": 1,
            "children": [
                {
                    "order": 1,
                    "title": "分组",
                    "slug": "/user/group",
                    "icon": "group",
                    "permission": "account.view_group",
                    "target": "_self",
                    "is_link": False,
                    "link": "",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                },
                {
                    "order": 2,
                    "title": "用户列表",
                    "slug": "/user/list",
                    "icon": "user-o",
                    "permission": "account.view_user",
                    "target": "_self",
                    "is_link": False,
                    "link": "",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                },
                {
                    "order": 3,
                    "title": "用户中心",
                    "slug": "/user/center",
                    "icon": "user-circle-o",
                    "permission": "",
                    "target": "_self",
                    "is_link": False,
                    "link": "",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                },
                {
                    "order": 4,
                    "title": "用户消息",
                    "slug": "/user/message",
                    "icon": "envelope-o",
                    "permission": "",
                    "target": "_self",
                    "is_link": False,
                    "link": "",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                },

            ]
        },
        {
            "order": 10,
            "title": "系统设置",
            "slug": "/config",
            "icon": "cog",
            "permission": "",
            "target": "_self",
            "is_link": False,
            "link": "",
            "is_deleted": False,
            "level": 1,
            "children": [
                {
                    "order": 1,
                    "title": "导航菜单",
                    "slug": "/config/menu",
                    "icon": "angle-right",
                    "permission": "config.view_menu",
                    "target": "_self",
                    "is_link": False,
                    "link": "",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                }
            ]
        },
        {
            "order": 20,
            "title": "友情链接",
            "slug": "/link",
            "icon": "link",
            "permission": "",
            "target": "_blank",
            "is_link": False,
            "link": "https://www.codelieche.com",
            "is_deleted": False,
            "level": 1,
            "children": [
                {
                    "order": 1,
                    "title": "编程列车",
                    "slug": "/codelieche",
                    "icon": "angle-right",
                    "permission": "",
                    "target": "_self",
                    "is_link": True,
                    "link": "https://www.codelieche.com",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                },
                {
                    "order": 5,
                    "title": "codelieche",
                    "slug": "/link/codelieche",
                    "icon": "angle-right",
                    "permission": "",
                    "target": "_blank",
                    "is_link": True,
                    "link": "https://www.codelieche.com",
                    "is_deleted": False,
                    "level": 2,
                    "children": []
                }
            ]
        }
    ]
    # 创建菜单
    for item in menus:
        menu = create_menu_item(item, None)
        print(menu)


def create_menu_item(data, parent):
    """
    创建单条菜单
    :param data: 字典对象
    :param parent: 父亲
    :return: Menu对象
    """
    # 1. 取出children
    children = data.pop("children")

    # 2. 创建当前菜单
    if parent:
        item = Menu.objects.create(**data, parent=parent)
    else:
        item = Menu.objects.create(**data)

    # 3. 创建子菜单
    if children and len(children) > 0:
        for c in children:
            create_menu_item(c, item)

    # 4. 返回：
    return item


def init_system_data():
    # 1. 检查用户
    check_user_or_create_superuser()
    # 2. 检查菜单
    check_menu_or_create_menus()


class ProjectSetupView(APIView):
    """
    项目数据初始化接口
    """

    def get(self, request):
        init_system_data()

        return JsonResponse({
            "status": True,
            "message": "初始化成功"
        })
