# -*- coding:utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Group

from account.models import User
from cmdb.models import Model, Permission


class PermissionModelSerializer(serializers.ModelSerializer):
    """
    数据权限 Model Serializer
    """

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Permission
        fields = (
            'id', 'name', 'groups', 'model', 'instances', 'can_view_all',
            'user', 'description', 'deleted', 'time_added',
        )


class PermissionInfoModelSerializer(serializers.ModelSerializer):
    """
    数据权限 Info Model Serializer
    """
    groups = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Group.objects.all(), required=False)
    model = serializers.SlugRelatedField(many=True, slug_field='code', queryset=Model.objects.filter(deleted=False),
                                         required=False)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        required=False, allow_null=True, )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Permission
        fields = (
            'id', 'name', 'groups', 'model', 'instances', 'can_view_all',
            'user', 'description', 'deleted', 'time_added',
        )
