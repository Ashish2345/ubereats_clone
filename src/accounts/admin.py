from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = [ "id", "first_name", "last_name", "email", "contact_no", "dob", "is_superuser"]
    list_filter = ["is_active", "is_admin", "gender"]
    search_fields = [ "id", "first_name", "last_name", "contact_no", "email"]


admin.site.register(User, UserAdmin)
