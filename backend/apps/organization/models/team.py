# -*- coding:utf-8 -*-
"""
ogranization：组织的Model
- Category: 类型、可自行添加，可以是：集团、公司、子公司、项目部、部门、小组等
- Team: 团体
- Role： 角色：自行定义：董事长、总经理、职员；甚至：开发、测试、运维都OK
- Member：角色
"""
from django.db import models


class Category(models.Model):
    """
    组织分类
    """
    name = models.CharField(verbose_name="名称", max_length=20, unique=True)
    code = models.SlugField(verbose_name="代码", max_length=20, unique=True)
    parent = models.ForeignKey(to="self", verbose_name="父级", blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)

    def __str__(self):
        return "分类:{}({})".format(self.name, self.code)

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
    parent = models.ForeignKey(to="self", verbose_name="父级", blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)

    def __str__(self):
        return "角色:{}({})".format(self.name, self.code)

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


class Team(models.Model):
    """
    团队
    """
    name = models.CharField(verbose_name="名称", max_length=128, unique=True)
    code = models.CharField(verbose_name="代码", max_length=20, unique=True)
    name_en = models.CharField(verbose_name="名称(英文)", max_length=128, blank=True, null=True)
    # 分类我们会设置个默认的为：Default
    category = models.ForeignKey(to="Category", verbose_name="分类", blank=True, null=True)
    parent = models.ForeignKey(to="self", verbose_name="父级", blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="级别", default=1, blank=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)

    # 团队的描述可能很长
    description = models.TextField(verbose_name="描述", max_length=256, blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="已删除", blank=True, default=False)

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
        verbose_name = "团队"
        verbose_name_plural = verbose_name
