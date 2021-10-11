# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from codelieche.tools.password import Cryptography


class BaseModel(models.Model):
    """
    Base Model
    添加了deleted字段，覆写了delete方法
    """
    delete_tasks = ()  # 需要执行的删除函数的任务（函数列表）
    SECRET_FIELDS = ()  # 需要加密的字段

    # 字段：删除、添加时间
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True, null=True)

    @staticmethod
    def strftime(fmt='%Y%m%d%H%M%S'):
        """
        格式化当前的时间戳，删除资源的时候会用到
        """
        return timezone.datetime.now().strftime(fmt)

    def set_decrypt_value(self):
        # 加密存储的字段
        if self.SECRET_FIELDS and isinstance(self.SECRET_FIELDS, (list, tuple)):
            p = Cryptography()

            # 自己配置SECRET_FIELDS, BaseModel中设置的是[]
            for i in self.SECRET_FIELDS:
                value = getattr(self, i)
                if i and value:
                    # 判断是否是加密的
                    success, _ = p.check_can_decrypt(value)
                    if not success:
                        setattr(self, i, p.encrypt(text=value))
            # 对需要加密的字段加密完毕

    def get_decrypt_value(self, field: str) -> str:
        """
        获取解密后的值
        """
        value = getattr(self, field)
        if value:
            p = Cryptography()
            success, de_p = p.check_can_decrypt(value=value)
            if success:
                return de_p
            else:
                return value

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 调用设置加密字段的方法
        self.set_decrypt_value()
        # 调用父类的save方法
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_relative_object_by_model(self, model, args=None, value=None, many=False, field="pk"):
        """
        通过model获取关系的对象
        多值还是单值，自行判断
        :param model: 类，必须是django的类
        :param args: 过滤条件，必须是dict
        :param value: 过滤检索的值，有可能是列表
        :param many: 是否是多值
        :param field: 过滤的字段，默认是pk
        :return:
        """
        # 1. 构造检索的数据
        # field自己处理，比如：id__in，等
        if args and isinstance(args, dict):
            data = args
        elif value:
            data = {field: value}
        else:
            raise ValueError("args或者value必须传递一个")

        # 2. 判断model是否正确
        if not issubclass(model, models.Model):
            raise ValueError("传入的model必须是django.db.Modeel的子类")

        # 3. 开始过滤数据
        if many:
            queryset = model.objects.filter(**data)
            return queryset
        else:
            # 这个直接用get是有可能报错的（比如根据一条字段，得到了2条数据），这个传入端去处理
            obj = model.objects.get(**data)
            return obj

    def get_relative_object_by_model(self, app_label, model, args=None, value=None, many=False, field="pk"):
        # 1. 先获取到model
        ct = ContentType.objects.get(app_label=app_label, model=model)
        model_cls = ct.model_class()

        # 2. 获取对象
        return self.get_relative_object_by_model(model=model_cls, args=args, value=value, many=many, field=field)

    def do_delete_action(self):
        """
        很多系统比如运维心态，所有数据都是只标记删除，而不做物理删除
        当我们删除的时候，需要执行可能需要执行额外的处理
        比如：把某个字段加个时间戳，删除额外的关联数据，比如关联了我的数据也需要删除掉
        """
        if self.deleted:
            # 1. 判断是否已经删除，如果已经是标记删除的了，那我们就直接返回
            return
        else:
            # 2. 遍历需要执行的删除的任务，我们对其进行删除
            if isinstance(self.delete_tasks, (list, tuple)):
                for i in self.delete_tasks:
                    # 别循环调用自己了
                    if i and hasattr(self, i) and i != 'do_delete_action':
                        task_func = getattr(self, i)
                        # 判断一下这个是否是函数
                        if hasattr(task_func, '__call__'):
                            # 我们执行调用函数
                            task_func()
                        else:
                            print('{}不是可调用的函数', i)
            self.deleted = True
            self.save(update_fields=('deleted',))

    def delete(self, using=None, keep_parents=False):
        # 1. 判断是否有do_delete_action的属性，且是可调用的
        if hasattr(self, "do_delete_action") and callable(self.do_delete_action):
            self.do_delete_action()
        else:
            # 如果没有就调用父类的删除方法，注意这里是调用models.Model的delete方法
            super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        # 抽象类
        abstract = True
