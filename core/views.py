from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ProfileForm, CustomUserCreationForm, NameCompletionForm, SkillForm
from .models import Profile, Skill


def home(request):
    # Get categories and gender choices for filter dropdown
    categories = Skill.SKILL_CATEGORIES
    gender_choices = Profile.GENDER_CHOICES

    context = {
        "categories": categories,
        "gender_choices": gender_choices,
    }
    return render(request, "core/home.html", context)


@login_required
def complete_name(request):
    """Allow existing users without names to add them (one-time only)"""
    if request.user.first_name and request.user.last_name:
        return redirect("profile_view")

    if request.method == "POST":
        form = NameCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    else:
        form = NameCompletionForm(instance=request.user)

    return render(request, "core/complete_name.html", {"form": form})


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "core/signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_view")
        return render(request, "core/signup.html", {"form": form})


@login_required
def profile_view(request, user_id=None):
    if user_id:
        target_user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=target_user)
        is_own_profile = target_user == request.user

        offered_skills = Skill.objects.filter(user=target_user, skill_type="offer")
        requested_skills = Skill.objects.filter(user=target_user, skill_type="request")

        context = {
            "profile": profile,
            "is_own_profile": is_own_profile,
            "offered_skills": offered_skills,
            "requested_skills": requested_skills,
        }
        return render(request, "core/public_profile_view.html", context)
    else:
        profile = get_object_or_404(Profile, user=request.user)

        offered_skills = Skill.objects.filter(user=request.user, skill_type="offer")
        requested_skills = Skill.objects.filter(user=request.user, skill_type="request")

        context = {
            "profile": profile,
            "completion_percentage": profile.completion_percentage,
            "is_complete": profile.is_profile_complete,
            "missing_fields": profile.missing_required_fields,
            "missing_critical_fields": profile.missing_critical_fields,
            "missing_skills_only": profile.missing_skills_only,
            "completion_status_type": profile.completion_status_type,
            "is_own_profile": True,
            "offered_skills": offered_skills,
            "requested_skills": requested_skills,
        }
        return render(request, "core/profile_view.html", context)


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        try:
            # Check completion status before saving
            was_complete_before = profile.is_profile_complete

            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()

                # Check if profile just became complete
                profile.refresh_from_db()
                is_complete_now = profile.is_profile_complete

                if not was_complete_before and is_complete_now:
                    # Profile just became complete
                    messages.success(request, "profile_completed")
                elif was_complete_before and is_complete_now:
                    # Profile was complete and remains complete (just updated)
                    messages.success(request, "profile_updated")
                elif not was_complete_before and not is_complete_now:
                    # Profile was incomplete and remains incomplete (but fields changed)
                    messages.success(request, "profile_updated")
                else:
                    # Fallback (shouldn't happen in normal flow)
                    messages.success(request, "Profile updated successfully!")

                return redirect("profile_view")
            else:
                messages.error(
                    request, "Please correct the errors below and try again."
                )

        except Exception as e:
            messages.error(
                request,
                "An error occurred while saving your profile. Please try again.",
            )
            print(f"Profile save error: {e}")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "core/profile_edit.html", {"form": form})


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


def search(request):
    # Get all users
    users_with_profiles = []
    users = (
        User.objects.filter(is_active=True)
        .exclude(is_superuser=True)
        .select_related("profile")
    )

    for user in users:
        try:
            profile = user.profile
            users_with_profiles.append({"user": user, "profile": profile})
        except Profile.DoesNotExist:
            continue

    context = {
        "users_with_profiles": users_with_profiles,
        "total_users": len(users_with_profiles),
        "show_complete_only": False,
    }
    return render(request, "core/search.html", context)


# Skill Views
@login_required
def skill_create(request):
    next_url = request.GET.get("next", "skill_list")
    skill_type = request.GET.get("type", "").strip()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()

            skill_type_display = skill.get_skill_type_display().lower()
            messages.success(
                request,
                f'Your {skill_type_display} "{skill.title}" has been created successfully!',
            )
            return redirect("skill_detail", pk=skill.pk)
    else:
        # Prefill form with skill_type from URL parameter
        initial_data = {}
        if skill_type in ["offer", "request"]:
            initial_data["skill_type"] = skill_type
        form = SkillForm(initial=initial_data)

    context = {
        "form": form,
        "next_url": next_url,
    }
    return render(request, "core/skill_create.html", context)


def skill_list(request):
    skills = Skill.objects.filter(is_active=True).select_related("user__profile")

    # Get filter parameters and clean them
    skill_type = request.GET.get("type", "").strip()
    category = request.GET.get("category", "").strip()
    search_query = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()
    gender = request.GET.get("gender", "").strip()

    if skill_type.lower() in ["none", "null", ""]:
        skill_type = ""
    if category.lower() in ["none", "null", ""]:
        category = ""
    if search_query.lower() in ["none", "null", ""]:
        search_query = ""
    if location.lower() in ["none", "null", ""]:
        location = ""
    if gender.lower() in ["none", "null", ""]:
        gender = ""

    # Filter by skill type (offer/request) - optional
    if skill_type and skill_type in ["offer", "request"]:
        skills = skills.filter(skill_type=skill_type)

    # Filter by category - optional
    if category and category != "":
        # Validate that the category exists in our choices
        valid_categories = [choice[0] for choice in Skill.SKILL_CATEGORIES]
        if category in valid_categories:
            skills = skills.filter(category=category)

    # Filter by location (city or country) - optional
    if location and location != "":
        skills = skills.filter(
            Q(user__profile__city__icontains=location)
            | Q(user__profile__country__icontains=location)
            | Q(location__icontains=location)
        )
    if gender and gender != "":
        valid_genders = [choice[0] for choice in Profile.GENDER_CHOICES]
        if gender in valid_genders:
            skills = skills.filter(user__profile__gender=gender)

    # Search functionality (optional - applies to title and description)
    if search_query and search_query != "":
        skills = skills.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    skills = skills.order_by("-created_at")

    # Pagination
    paginator = Paginator(skills, 12)  # Show 12 skills per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get categories and gender choices for filter dropdowns
    categories = Skill.SKILL_CATEGORIES
    gender_choices = Profile.GENDER_CHOICES

    context = {
        "page_obj": page_obj,
        "skills": page_obj,
        "categories": categories,
        "gender_choices": gender_choices,
        "current_type": skill_type if skill_type else "",
        "current_category": category if category else "",
        "current_location": location if location else "",
        "current_gender": gender if gender else "",
        "search_query": search_query if search_query else "",
        "total_skills": skills.count(),
    }

    return render(request, "core/skill_list.html", context)


def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk, is_active=True)

    other_skills = Skill.objects.filter(user=skill.user, is_active=True).exclude(pk=pk)[
        :3
    ]

    context = {
        "skill": skill,
        "other_skills": other_skills,
        "can_edit": request.user == skill.user,
    }

    return render(request, "core/skill_detail.html", context)


@login_required
def skill_edit(request, pk):
    """Edit an existing skill listing"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    next_url = request.GET.get("next", "skill_detail")

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your skill "{skill.title}" has been updated successfully!'
            )
            return redirect("skill_detail", pk=skill.pk)
    else:
        form = SkillForm(instance=skill)

    context = {
        "form": form,
        "skill": skill,
        "is_edit": True,
        "next_url": next_url,
    }

    return render(request, "core/skill_create.html", context)


@login_required
def skill_delete(request, pk):
    """Delete a skill listing"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)

    if request.method == "POST":
        skill_title = skill.title
        skill.delete()
        messages.success(
            request, f'Your skill "{skill_title}" has been deleted successfully!'
        )
        return redirect("skill_list")

    return render(request, "core/skill_delete.html", {"skill": skill})


@login_required
def my_skills(request):
    skills = Skill.objects.filter(user=request.user, is_active=True).order_by(
        "-created_at"
    )

    context = {
        "skills": skills,
        "offers_count": skills.filter(skill_type="offer").count(),
        "requests_count": skills.filter(skill_type="request").count(),
    }

    return render(request, "core/my_skills.html", context)
