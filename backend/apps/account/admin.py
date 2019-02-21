from django.contrib import admin
from account.models import User
# Register your models here.


class UserModelAdmin(admin.ModelAdmin):
    """
    User Model Admin
    """
    list_display = ("id", "username", "nick_name", "id_card", "mobile", "email", "gender", "can_view")
    search_fields = ("username", "nick_name", "id_card")
    list_filter = ("gender", "can_view")


admin.site.register(User, UserModelAdmin)
