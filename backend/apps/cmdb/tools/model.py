# -*- coding:utf-8 -*-

from cmdb.models.model import Model


def get_model_by_name(name: str, deleted: bool=False):
    """
    通过名字获取Model
    :param name: 名字
    :param deleted: 是否删除，默认为False
    :return: Model对象或者None
    """
    if deleted:
        return Model.objects.filter(name=name, deleted=False).first()
    else:
        return Model.objects.filter(name=name, deleted=True).first()


def get_model_by_id(pk: int, deleted: bool = False):
    """
    通过ID获取Model
    :param pk: Model的ID
    :param deleted: 是否删除，默认为False
    :return: Model对象或者None
    """
    if deleted:
        return Model.objects.filter(id=pk, deleted=False).first()
    else:
        return Model.objects.filter(id=pk, deleted=True).first()
