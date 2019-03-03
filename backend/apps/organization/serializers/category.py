# -*- coding:utf-8 -*-
"""
Oragination Team Serializers
"""
from rest_framework import serializers

from organization.models.team import Category


class CategorySimpleModelSerializer(serializers.ModelSerializer):
    """
    Category Simple Model Serializer
    """

    class Meta:
        model = Category
        fields = ("id", "name", "code")


class CategoryModelSerializer(serializers.ModelSerializer):
    """
    Category Model Serializer
    """
    subs = CategorySimpleModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "code", "parent", "is_deleted", "description", "subs")


class CategoryDetailModelSerializer(serializers.ModelSerializer):
    """
    Category Detail Model Serializer
    """
    parent = serializers.SlugRelatedField(slug_field="name", read_only=True)
    subs = CategoryModelSerializer(many=True, read_only=True)
    # subs = CategorySimpleModelSerializer(many=True, read_only=True)
    # subs = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "code", "parent", "is_deleted", "description", "subs")
