from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile


def home(request):
    return render(request, "core/home.html")


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "core/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
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
