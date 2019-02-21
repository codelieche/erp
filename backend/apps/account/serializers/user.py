# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User


class UserLoginSerializer(serializers.Serializer):
    """用户登录 Serializer"""
    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)


class UserSimpleInfoSerializer(serializers.ModelSerializer):
    """
    用户基本信息Model Serializer
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name')


class UserAllListSerializer(serializers.ModelSerializer):
    """
    列出所有用户的信息Model Serializer
    """
    parent = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'id_card', 'mobile', 'dingding', 'wechart', "ucode", "parent",
                  'is_superuser', 'is_active', 'can_view', 'last_login', 'is_deleted', "date_joined")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情/编辑序列化Model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'id_card', 'is_active', 'mobile',
                  'dingding', 'wechart', 'ucode', 'can_view',
                  'is_superuser', 'last_login', 'is_deleted')
        read_only_fields = ('id', 'username', 'last_login')


class UserModelSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    def create(self, validated_data):
        request = self.context["request"]
        # 密码校验
        password = request.data.get("password")
        repassword = request.data.get("repassword")

        if password and repassword:
            if password != repassword:
                raise serializers.ValidationError("输入的密码不相同")
        else:
            raise serializers.ValidationError("请输入密码")

        ucode = request.query_params.get("ucode")
        instance = super().create(validated_data=validated_data)
        if ucode:
            parent = User.objects.filter(ucode=ucode).first()
            instance.parent = parent
            # instance.save()
        # 设置密码
        instance.set_password(password)
        instance.nick_name = instance.username
        instance.can_view = False
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "email", "username", "nick_name", 'id_card', "mobile", "qq", "wechart")
