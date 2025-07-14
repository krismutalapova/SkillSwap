from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm, CustomUserCreationForm, NameCompletionForm
from .models import Profile


def home(request):
    return render(request, "core/home.html")


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
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    context = {
        "profile": profile,
        "completion_percentage": profile.completion_percentage,
        "is_complete": profile.is_profile_complete,
        "missing_fields": profile.missing_required_fields,
        "missing_critical_fields": profile.missing_critical_fields,
        "missing_skills_only": profile.missing_skills_only,
        "completion_status_type": profile.completion_status_type,
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

                from django.contrib import messages

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
    # Get all users with complete profiles only
    users_with_profiles = []
    users = (
        User.objects.filter(is_active=True)
        .exclude(is_superuser=True)
        .select_related("profile")
    )

    for user in users:
        try:
            profile = user.profile
            # Only include users with complete profiles
            if profile.is_profile_complete:
                users_with_profiles.append({"user": user, "profile": profile})
        except Profile.DoesNotExist:
            continue

    context = {
        "users_with_profiles": users_with_profiles,
        "total_users": len(users_with_profiles),
        "show_complete_only": True,
    }
    return render(request, "core/search.html", context)
