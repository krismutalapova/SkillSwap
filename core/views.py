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
    return render(request, "core/profile_view.html", {"profile": profile})


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "core/profile_edit.html", {"form": form})


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


def search(request):
    # Get all users with their profiles
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
    }
    return render(request, "core/search.html", context)
