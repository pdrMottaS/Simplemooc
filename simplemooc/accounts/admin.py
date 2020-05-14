from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):

    list_display=['username','email','name']
    search_fields=['name','email']

admin.site.register(User,UserAdmin)
