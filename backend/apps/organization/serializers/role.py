# -*- coding:utf-8 -*-
"""
Oragination Team Role Serializers
"""
from rest_framework import serializers

from organization.models.team import Role


class RoleSimpleModelSerializer(serializers.ModelSerializer):
    """
    Role Simple Model Serializer
    """

    class Meta:
        model = Role
        fields = ("id", "name", "code")


class RoleModelSerializer(serializers.ModelSerializer):
    """
    Role Model Serializer
    """
    subs = RoleSimpleModelSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ("id", "name", "code", "parent", "is_deleted", "description", "subs")


class RoleDetailModelSerializer(serializers.ModelSerializer):
    """
    Role Detail Model Serializer
    """
    parent = serializers.SlugRelatedField(slug_field="name", read_only=True)
    subs = RoleModelSerializer(many=True, read_only=True)
    # subs = RoleSimpleModelSerializer(many=True, read_only=True)
    # subs = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Role
        fields = ("id", "name", "code", "parent", "is_deleted", "description", "subs")
