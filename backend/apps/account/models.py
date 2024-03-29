from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.


class UserProfile(AbstractUser):
    """
    自定义的用户Model
    拓展字段gender, nick_name, mobile, qq
    """

    GENDER_CHOICES = (
        ('male', "男"),
        ('female', "女"),
        ('secret', "保密")
    )

    nick_name = models.CharField(max_length=40, blank=True, verbose_name="昵称")
    # 头像url
    avatar = models.CharField(verbose_name="头像", blank=True, null=True, max_length=256)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="secret",
                              verbose_name="性别")
    # email可以随便填，但是手机号需要唯一: 后续可加入校验验证码
    mobile = models.CharField(max_length=11, verbose_name="手机号", unique=True)
    qq = models.CharField(max_length=12, verbose_name="QQ号", blank=True, null=True)
    # 公司有时候会用到钉钉/微信发送消息，需要记录用户相关ID
    dingding = models.CharField(max_length=40, verbose_name="钉钉ID", blank=True, null=True)
    wechat = models.CharField(max_length=40, verbose_name="微信ID", blank=True, null=True)
    # 能否访问本系统，默认是不可以访问本系统
    # 注意第一个管理员用户，可以去数据库调整can_view的值为1
    can_view = models.BooleanField(verbose_name="能访问", default=False, blank=True)
    is_deleted = models.BooleanField(verbose_name="删除", default=False, blank=True)

    def __repr__(self):
        return "UserProfile:{}".format(self.username)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


# 注意：get_user_model()方法可以获取到本系统使用的是哪个用户Model
# 默认的用户Model是：django.contrib.auth.models.User
# 在settings.py中配置：AUTH_USER_MODEL可以修改成指定的用户Model
# AUTH_USER_MODEL = "account.UserProfile"
User = get_user_model()
# 注意这句是要放在class UserProfile后面的


class MessageScope(models.Model):
    """
    消息范围
    """
    scope = models.SlugField(verbose_name="范围", max_length=10)
    name = models.CharField(verbose_name="范围名称", max_length=10, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.name:
            self.name = self.scope
            super().save(force_insert=force_insert, force_update=force_update,
                         using=using, update_fields=update_fields)

    def __str__(self):
        return "Message:{}".format(self.scope)

    class Meta:
        verbose_name = "消息范围"
        verbose_name_plural = verbose_name


class Message(models.Model):
    """
    用户消息Model
    """
    user = models.ForeignKey(to=User, verbose_name='用户', on_delete=models.CASCADE)
    sender = models.CharField(max_length=15, verbose_name="发送者", default='system', blank=True)
    # 消息类型，想用type，但是还是用scope，type和types是mysql的预保留字
    scope = models.ForeignKey(to=MessageScope, verbose_name="消息范围", blank=True,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="消息标题")
    content = models.CharField(max_length=512, verbose_name="消息内容", blank=True)
    link = models.CharField(max_length=128, verbose_name="链接", blank=True, null=True)
    unread = models.BooleanField(verbose_name="未读", blank=True, default=True)
    time_added = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    is_deleted = models.BooleanField(verbose_name="删除", default=False, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 当content为空的时候，让其等于title
        if not self.content:
            self.content = self.title
        # 设置scope
        if not self.scope:
            scope, created = MessageScope.objects.get_or_create(scope="default")
            self.scope = scope

        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)

    def __repr__(self):
        return 'Message({})'.format(self.pk)

    def __str__(self):
        return "用户消息:{}-{}".format(self.user.username, self.pk)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name
