# -*- coding:utf-8 -*-
"""
ogranization：组织的Model
- Category: 类型、可自行添加，可以是：集团、公司、子公司、项目部、部门、小组等
- Team: 团体
- Role： 角色：自行定义：董事长、总经理、职员；甚至：开发、测试、运维都OK
- Member：成员
- MemberShip: 角色成员关系
"""
from django.db import models

from account.models import User


class Category(models.Model):
    """
    组织分类
    """
    name = models.CharField(verbose_name="名称", max_length=20, unique=True)
    code = models.SlugField(verbose_name="代码", max_length=20, unique=True)
    parent = models.ForeignKey(to="self", verbose_name="父级", blank=True, null=True, on_delete=models.CASCADE)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)

    def __str__(self):
        return "组织分类:{}({})".format(self.name, self.code)

    @property
    def subs(self):
        if self.category_set.count() > 0:
            return self.category_set.all()
        else:
            return []

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 1. 计算level
        level = 1
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        self.level = level
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name="名称", max_length=20, unique=True)
    code = models.SlugField(verbose_name="代码", max_length=20, unique=True)
    parent = models.ForeignKey(to="self", verbose_name="父级", on_delete=models.CASCADE, blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)

    def __str__(self):
        return "角色:{}({})".format(self.name, self.code)

    @property
    def subs(self):
        if self.role_set.count() > 0:
            return self.role_set.all()
        else:
            return []

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 1. 计算level
        level = 1
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        self.level = level
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class Team(models.Model):
    """
    团队/团体/组织
    """
    name = models.CharField(verbose_name="名称", max_length=128, unique=True)
    code = models.CharField(verbose_name="代码", max_length=20, unique=True)
    name_en = models.CharField(verbose_name="名称(英文)", max_length=128, blank=True, null=True)
    # 分类我们会设置个默认的为：Default
    category = models.ForeignKey(to="Category", verbose_name="分类", on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(to="self", verbose_name="父级", on_delete=models.CASCADE, blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)
    # 团队的描述可能很长
    description = models.TextField(verbose_name="描述", blank=True, null=True)

    def __str__(self):
        return "{}({})".format(self.name, self.code)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 需要自行计算这个团队的级别、检查分类，如果没有就设置为默认
        # 1. 计算level
        level = 1
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        self.level = level

        # 2. 设置分组类型
        if not self.category:
            default = Category.objects.filter(code="default").first()
            if not default:
                default = Category.objects.create(code="default", name="Default")
            # 设置分类为default
            self.category = default

        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    class Meta:
        verbose_name = "团队/团体/组织"
        verbose_name_plural = verbose_name


class Member(models.Model):
    """
    成员
    """
    team = models.ForeignKey(to="Team", verbose_name="团体", on_delete=models.CASCADE)
    role = models.ForeignKey(to="Role", verbose_name="角色", on_delete=models.CASCADE)
    users = models.ManyToManyField(to=User, verbose_name="用户", through="MemberShip")
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)
    description = models.CharField(verbose_name="描述", blank=True, max_length=256)

    def __str__(self):
        return "{}-{}(角色)".format(self.team.name, self.role.name)

    class Meta:
        verbose_name = "团队成员(角色)"
        verbose_name_plural = verbose_name


class MemberShip(models.Model):
    """"""
    member = models.ForeignKey(to=Member, verbose_name="成员", on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, verbose_name="用户", on_delete=models.CASCADE)
    is_leader = models.BooleanField(verbose_name="是否是Leader", default=False, blank=True)
    is_active = models.BooleanField(verbose_name="是否激活", default=True, blank=True)
    # 成员有加入时间，也有离开时间，离开后又重新加入等
    # 也可以弄个日志的Model记录成员的加入离开事件信息
    time_joined = models.DateTimeField(verbose_name="加入时间", auto_now_add=True, blank=True)
    time_leaved = models.DateTimeField(verbose_name="离开时间", blank=True, null=True)
    description = models.CharField(verbose_name="描述", blank=True, max_length=256)

    def __str__(self):
        return "{}_{}_{}(成员)".format(self.member.team.name, self.member.role.name, self.user.username)

    class Meta:
        verbose_name = "团队成员(关系)"
        verbose_name_plural = verbose_name
