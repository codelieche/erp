# -*- coding:utf-8 -*-
"""
导航数据：管理员和普通用户
后面应该改成可配置的，但是暂时先使用这种方式
"""

icon, key, title, subs, slug = 'icon', 'key', 'title', 'subs', 'slug'

superuser_nav = [
    {
        icon: 'tool',
        key: 'storage',
        title: '进销存',
        subs: [
            {
                slug: '/storage/store',
                icon: 'right',
                title: '仓库点',
            },
            {
                slug: '/storage/out',
                icon: 'right',
                title: '出库记录',
            },
            {
                slug: '/storage/input',
                icon: 'right',
                title: '入库记录',
            },
        ]
    },
    {
        icon: 'team',
        key: 'user',
        title: '用户中心',
        subs: [
            {
                slug: '/user/group',
                icon: 'usergroup-add',
                title: '分组',
            },
            {
                slug: '/user/list',
                icon: 'usergroup-add',
                title: '用户列表',
            },
            {
                slug: '/user/message',
                icon: 'message',
                title: '消息中心',
            },
            {
                slug: '/user/login',
                icon: 'user',
                title: '登陆',
            },
            {
                slug: '/user/logout',
                icon: 'logout',
                title: '退出',
            },
        ]
    }
]

normal_user_nav = [
    {
        icon: 'tool',
        key: 'storage',
        title: '进销存',
        subs: [
            {
                slug: '/storage/store',
                icon: 'right',
                title: '仓库点',
            },
            {
                slug: '/storage/out',
                icon: 'right',
                title: '出库记录',
            },
            {
                slug: '/storage/input',
                icon: 'right',
                title: '入库记录',
            },
        ]
    },
    {
        icon: 'team',
        key: 'user',
        title: '用户中心',
        subs: [
            {
                slug: '/user/message',
                icon: 'message',
                title: '消息中心',
            },
            {
                slug: '/user/login',
                icon: 'user',
                title: '登陆',
            },
            {
                slug: '/user/logout',
                icon: 'logout',
                title: '退出',
            },
        ]
    }
]
