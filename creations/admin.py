from django.contrib import admin
from .models import Creation

@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "publishedAt", "isPublished")
    list_filter = ("kind", "isPublished")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "bodyMarkdown")
