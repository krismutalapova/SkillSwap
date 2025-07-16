from django.contrib import admin
from .models import Profile, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "city",
        "country",
        "completion_percentage",
        "is_profile_complete",
    )
    list_filter = ("gender", "country")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "city",
        "country",
    )
    readonly_fields = (
        "completion_percentage",
        "is_profile_complete",
        "missing_required_fields",
    )

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Profile Details",
            {"fields": ("bio", "profile_picture", "city", "country", "gender")},
        ),
        ("Skills", {"fields": ("skills_offered", "skills_needed")}),
        (
            "Profile Status",
            {
                "fields": (
                    "completion_percentage",
                    "is_profile_complete",
                    "missing_required_fields",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "skill_type",
        "category",
        "is_remote",
        "is_active",
        "created_at",
    )
    list_filter = ("skill_type", "category", "is_remote", "is_active", "created_at")
    search_fields = (
        "title",
        "description",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("user", "title", "description")}),
        ("Classification", {"fields": ("skill_type", "category")}),
        ("Details", {"fields": ("location", "availability", "is_remote")}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
