from django.contrib import admin

from journal.models import Journal

# Register your models here.
@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_private', 'message', 'image', 'file')