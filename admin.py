from django.contrib import admin
from blog.models import Entry

# Register your models here.
class EntryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Entry, EntryAdmin)