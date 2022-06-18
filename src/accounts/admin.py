from django.contrib import admin

from .models import User, UserToken, Test

class UserAdmin(admin.ModelAdmin):
    list_display = [ "id", "first_name", "last_name", "email", "contact_no", "dob", "is_superuser"]
    list_filter = ["is_active", "is_admin", "gender"]
    search_fields = [ "id", "first_name", "last_name", "contact_no", "email"]

class UserTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "token", "exipired_at"]
    search_fields = ["id", "user_id",]


admin.site.register(User, UserAdmin)
admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(Test)
