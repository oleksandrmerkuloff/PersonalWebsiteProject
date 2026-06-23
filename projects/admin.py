from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    fields = ["name", "description", "project_url"]
    list_display = ["name", "created_at"]
    list_display_links = ["name"]
    list_per_page = 50
    search_fields = ["name"]
    sortable_by = ["name", "created_at", "updated_at"]    
