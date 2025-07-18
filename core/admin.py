from django.contrib import admin
from .models import Profile, Skill, Rating, Message


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


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "skill",
        "user",
        "rating",
        "created_at",
    )
    list_filter = ("rating", "created_at", "skill__skill_type", "skill__category")
    search_fields = (
        "skill__title",
        "user__username",
        "user__first_name",
        "user__last_name",
        "comment",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Rating Information", {"fields": ("skill", "user", "rating")}),
        ("Comment", {"fields": ("comment",)}),
        ("Timestamp", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("skill", "user")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "skill",
        "subject",
        "is_read",
        "created_at",
    )
    list_filter = ("is_read", "created_at")
    search_fields = (
        "sender__username",
        "receiver__username",
        "subject",
        "skill__title",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Message Information", {"fields": ("sender", "receiver", "skill")}),
        ("Content", {"fields": ("subject", "message")}),
        ("Status", {"fields": ("is_read",)}),
        ("Timestamp", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("sender", "receiver", "skill")
        )
