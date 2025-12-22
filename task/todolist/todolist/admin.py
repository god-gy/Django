from django.contrib import admin

from .models import ToDoList, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('user', 'massage')
    extra = 1

@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'is_complete', 'start_date', 'end_date')
    list_display_links = ('id', 'title')
    list_filter = ('is_complete',)
    ordering = ('start_date',)
    inlines = [
        CommentInline
    ]
