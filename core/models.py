from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("P", "Prefer not to say"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills_offered = models.TextField(blank=True)
    skills_needed = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def is_profile_complete(self):
        required_user_fields = bool(self.user.first_name and self.user.last_name)
        required_profile_fields = bool(
            self.city
            and self.country
            and (self.skills_offered.strip() or self.skills_needed.strip())
        )
        return required_user_fields and required_profile_fields

    @property
    def completion_percentage(self):
        total_fields = 8
        completed_fields = 0
        if self.user.first_name:
            completed_fields += 1
        if self.user.last_name:
            completed_fields += 1
        if self.bio.strip():
            completed_fields += 1
        if self.skills_offered.strip():
            completed_fields += 1
        if self.skills_needed.strip():
            completed_fields += 1
        if self.city:
            completed_fields += 1
        if self.country:
            completed_fields += 1
        if self.profile_picture:
            completed_fields += 1

        return round((completed_fields / total_fields) * 100)

    @property
    def missing_required_fields(self):
        missing = []
        if not self.user.first_name:
            missing.append("First Name")
        if not self.user.last_name:
            missing.append("Last Name")
        if not self.city:
            missing.append("City")
        if not self.country:
            missing.append("Country")
        if not (self.skills_offered.strip() or self.skills_needed.strip()):
            missing.append("Skills (offered or needed)")
        return missing

    @property
    def missing_critical_fields(self):
        missing = []
        if not self.user.first_name:
            missing.append("First Name")
        if not self.user.last_name:
            missing.append("Last Name")
        if not self.city:
            missing.append("City")
        if not self.country:
            missing.append("Country")
        return missing

    @property
    def missing_skills_only(self):
        has_critical_missing = bool(self.missing_critical_fields)
        has_skills = bool(self.skills_offered.strip() or self.skills_needed.strip())
        return not has_critical_missing and not has_skills

    @property
    def completion_status_type(self):
        if self.is_profile_complete:
            return "complete"
        elif self.missing_critical_fields:
            return "critical_missing"
        elif self.missing_skills_only:
            return "skills_missing"
        else:
            return "critical_missing"

    def update_skills_from_skill_objects(self):
        offered_skills = self.user.skills.filter(
            skill_type="offer", is_active=True
        ).values_list("title", flat=True)

        needed_skills = self.user.skills.filter(
            skill_type="request", is_active=True
        ).values_list("title", flat=True)

        self.skills_offered = ", ".join(offered_skills)
        self.skills_needed = ", ".join(needed_skills)
        self.save()


class Skill(models.Model):
    SKILL_TYPES = [
        ("offer", "Skill Offered"),
        ("request", "Skill Requested"),
    ]

    SKILL_CATEGORIES = [
        ("technology", "IT, Programming & Tech"),
        ("languages", "Languages"),
        ("music", "Music & Arts"),
        ("sports", "Sports & Fitness"),
        ("cooking", "Cooking & Food"),
        ("crafts", "Crafts & DIY"),
        ("academic", "Academic & Education"),
        ("business", "Business & Finance"),
        ("health", "Health & Wellness"),
        ("fashion", "Fashion & Beauty"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=200)
    description = models.TextField()
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPES)
    category = models.CharField(
        max_length=20, choices=SKILL_CATEGORIES, default="other"
    )
    location = models.CharField(
        max_length=200, blank=True, help_text="Where can this skill be taught/learned?"
    )
    availability = models.CharField(
        max_length=200, blank=True, help_text="When are you available?"
    )
    is_remote = models.BooleanField(
        default=False, help_text="Can this be done remotely/online?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_skill_type_display()}: {self.title}"

    def get_absolute_url(self):
        return reverse("skill_detail", kwargs={"pk": self.pk})


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=Skill)
def update_profile_skills_on_save(sender, instance, **kwargs):
    instance.user.profile.update_skills_from_skill_objects()


@receiver(models.signals.post_delete, sender=Skill)
def update_profile_skills_on_delete(sender, instance, **kwargs):
    instance.user.profile.update_skills_from_skill_objects()
