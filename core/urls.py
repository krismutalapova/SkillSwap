from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.http import Http404
from .views import SignupView, home, profile_view, profile_edit


def redirect_to_home(request):
    return redirect("home")


urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home_alt"),
    path("index/", redirect_to_home, name="index_redirect"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="core/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="core/logout.html", next_page=None),
        name="logout",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", profile_view, name="profile_view"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("test-404/", lambda request: render(request, "404.html"), name="test_404"),
    path("test-500/", lambda request: render(request, "500.html"), name="test_500"),
    path(
        "simulate-404/",
        lambda request: (_ for _ in ()).throw(Http404("Test 404 error")),
        name="simulate_404",
    ),
]
