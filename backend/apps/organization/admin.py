from django.contrib import admin

from organization.models.team import Category, Team, Role, Member, MemberShip

# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    """
    Category Model Admin
    """
    list_display = ("id", "level", "name", "code", "parent", "description", "time_added", "is_deleted")
    search_fields = ("name", "description")


class TeamModelAdmin(admin.ModelAdmin):
    """
    Team Model Admin
    """
    list_display = ("id", "level", "name", "code", "name_en", "category", "time_added")
    search_fields = ("name",)


class RoleModelAdmin(admin.ModelAdmin):
    """
    Role Model Admin
    """
    list_display = ("id", "level", "name", "parent", "description", "time_added", "is_deleted")
    search_fields = ("name", "description")


class MemberModelAdmin(admin.ModelAdmin):
    """
    Member Model Admin
    """
    list_display = ("id", "team", "role")


class MemberShipModelAdmin(admin.ModelAdmin):
    """
    Member Ship Model Admin
    """
    list_display = ("id", "member", "user", "is_leader", "is_active", "time_joined", "time_leaved", "description")


# 注册admin
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Team, TeamModelAdmin)
admin.site.register(Role, RoleModelAdmin)
admin.site.register(Member, MemberModelAdmin)
admin.site.register(MemberShip, MemberShipModelAdmin)
