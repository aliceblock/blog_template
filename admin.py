from django.contrib import admin
from blog.models import Entry, Tag

# Register your models here.
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','updated_on','view','comment_counter','is_published')
    #exclude = ('slug',)

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)