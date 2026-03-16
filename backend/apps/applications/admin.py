from django.contrib import admin

from .models import JobApplication, SavedJob, SwipeEvent


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "job",
        "method",
        "status",
        "match_score",
        "confirmation_email_sent",
    )
    list_filter = ("method", "status", "confirmation_email_sent")
    search_fields = ("profile__user__username", "job__title", "job__company")


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("profile", "job", "created_at")
    search_fields = ("profile__user__username", "job__title", "job__company")


@admin.register(SwipeEvent)
class SwipeEventAdmin(admin.ModelAdmin):
    list_display = ("profile", "job", "action", "created_at")
    list_filter = ("action",)
    search_fields = ("profile__user__username", "job__title", "job__company")
