from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import (
    ProfileForm,
    CustomUserCreationForm,
    NameCompletionForm,
    SkillForm,
    MessageForm,
    RatingForm,
)
from .models import Profile, Skill, Message, Rating


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

    return render(request, "core/auth/complete_name.html", {"form": form})


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "core/auth/signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_view")
        return render(request, "core/auth/signup.html", {"form": form})


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
        return render(request, "core/profiles/public_profile_view.html", context)
    else:
        profile = get_object_or_404(Profile, user=request.user)

        offered_skills = Skill.objects.filter(user=request.user, skill_type="offer")
        requested_skills = Skill.objects.filter(user=request.user, skill_type="request")

        context = {
            "profile": profile,
            "is_own_profile": True,
            "offered_skills": offered_skills,
            "requested_skills": requested_skills,
        }
        return render(request, "core/profiles/profile_view.html", context)


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        try:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
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

    # Get user's skills for display
    offered_skills = Skill.objects.filter(user=request.user, skill_type="offer")
    requested_skills = Skill.objects.filter(user=request.user, skill_type="request")

    return render(
        request,
        "core/profiles/profile_edit.html",
        {
            "form": form,
            "profile": profile,
            "offered_skills": offered_skills,
            "requested_skills": requested_skills,
        },
    )


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
    return render(request, "core/skills/skill_create.html", context)


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

    return render(request, "core/skills/skill_list.html", context)


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

    return render(request, "core/skills/skill_detail.html", context)


@login_required
def skill_edit(request, pk):
    """Edit an existing skill listing"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    next_url = request.GET.get("next", "skill_detail")

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("skill_detail", pk=skill.pk)
    else:
        form = SkillForm(instance=skill)

    context = {
        "form": form,
        "skill": skill,
        "is_edit": True,
        "next_url": next_url,
    }

    return render(request, "core/skills/skill_create.html", context)


@login_required
def skill_delete(request, pk):
    """Delete a skill listing"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)

    if request.method == "POST":
        skill_title = skill.title
        skill.delete()
        return redirect("skill_list")

    return render(request, "core/skills/skill_delete.html", {"skill": skill})


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

    return render(request, "core/skills/my_skills.html", context)


# Messaging Views


@login_required
def send_message(request, skill_id=None, user_id=None):
    skill = None
    receiver = None

    if skill_id:
        # Skill-specific message
        skill = get_object_or_404(Skill, id=skill_id)
        receiver = skill.user
        redirect_url = "skill_detail"
        redirect_kwargs = {"pk": skill.id}
    elif user_id:
        # General message to user
        receiver = get_object_or_404(User, id=user_id)
        redirect_url = "public_profile_view"
        redirect_kwargs = {"user_id": user_id}
    else:
        messages.error(request, "Invalid message request.")
        return redirect("home")

    if receiver == request.user:
        messages.error(request, "You cannot send a message to yourself.")
        return redirect(redirect_url, **redirect_kwargs)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            if skill:
                message.skill = skill
            message.save()

            return redirect(redirect_url, **redirect_kwargs)
    else:
        if skill:
            initial_subject = f"Interested in: {skill.title}"
        else:
            initial_subject = f"Message from {request.user.first_name}"
        form = MessageForm(initial={"subject": initial_subject})

    context = {
        "form": form,
        "skill": skill,
        "receiver": receiver,
    }
    return render(request, "core/messaging/send_message.html", context)


@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by(
        "-created_at"
    )

    # Pagination
    paginator = Paginator(received_messages, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "messages": page_obj,
        "unread_count": received_messages.filter(is_read=False).count(),
    }
    return render(request, "core/messaging/inbox.html", context)


@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by("-created_at")

    # Pagination
    paginator = Paginator(sent_messages, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "messages": page_obj,
    }
    return render(request, "core/messaging/sent_messages.html", context)


@login_required
def view_message(request, message_id):
    """View a specific message"""
    message = get_object_or_404(Message, id=message_id)

    # Check if user is sender or receiver
    if message.sender != request.user and message.receiver != request.user:
        messages.error(request, "You don't have permission to view this message.")
        return redirect("inbox")

    # Mark as read if user is the receiver
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()

    context = {
        "message": message,
    }
    return render(request, "core/messaging/view_message.html", context)


# Rating Views


@login_required
def rate_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if skill.user == request.user:
        messages.error(request, "You cannot rate your own skill.")
        return redirect("skill_detail", pk=skill.id)

    existing_rating = Rating.objects.filter(skill=skill, user=request.user).first()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.skill = skill
            rating.user = request.user
            rating.save()

            action = "updated" if existing_rating else "submitted"
            return redirect("skill_detail", pk=skill.id)
    else:
        form = RatingForm(instance=existing_rating)

    context = {
        "form": form,
        "skill": skill,
        "existing_rating": existing_rating,
    }
    return render(request, "core/components/rate_skill.html", context)
