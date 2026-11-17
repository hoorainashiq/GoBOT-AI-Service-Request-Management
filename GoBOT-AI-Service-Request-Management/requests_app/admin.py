from django.contrib import admin

from .models import Comment, ServiceRequest


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "priority", "status", "requester", "assigned_to", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description", "requester__username")
    inlines = [CommentInline]
