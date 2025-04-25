from django.contrib import admin
from buddies.models import Buddy

class BuddyAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'species', 'xp', 'owner', 'fic']

admin.site.register(Buddy, BuddyAdmin)