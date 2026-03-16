from django.contrib import admin

from .models import CandidateProfile


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "headline",
        "location",
        "experience_years",
        "auto_apply_enabled",
        "auto_apply_threshold",
    )
    search_fields = ("user__username", "user__email", "headline", "location")
    list_filter = ("auto_apply_enabled",)
