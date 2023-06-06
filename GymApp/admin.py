from django.apps import AppConfig
from django.contrib import admin
from django.contrib.auth.models import Group

from GymApp.models import GymUser, Mail


class GymUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'weight', 'height', 'picture',)
    filter_horizontal = ('groups',)
    exclude = ('user_permissions', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'password',
               'notifications')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)


class MailAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'message', 'created_at')
    readonly_fields = ('email', 'title', 'message', 'created_at')
    search_fields = ('email', 'title', 'message', 'created_at')
    ordering = ('-created_at',)


# Change the title of the admin site
admin.site.site_header = "Pannello di amministrazione"
admin.site.site_title = "Admin Area"
admin.site.index_title = "Gestisci la tua palestra"

admin.site.register(Mail, MailAdmin)
admin.site.register(GymUser, GymUserAdmin)
admin.site.unregister(Group)
