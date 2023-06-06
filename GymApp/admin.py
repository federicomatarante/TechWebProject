from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from GymApp.models import GymUser, Mail


class GymUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'weight', 'height', 'picture')

class MailAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'message')
    readonly_fields = ('email', 'title', 'message')

admin.site.register(GymUser, GymUserAdmin)
admin.site.register(Mail, MailAdmin)