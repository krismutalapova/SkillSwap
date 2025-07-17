from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.http import Http404
from .views import (
    SignupView,
    home,
    profile_view,
    profile_edit,
    search,
    complete_name,
    skill_create,
    skill_list,
    skill_detail,
    skill_edit,
    skill_delete,
    my_skills,
)


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
    path("search/", search, name="search"),
    path("profile/", profile_view, name="profile_view"),
    path("profile/<int:user_id>/", profile_view, name="public_profile_view"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("profile/complete-name/", complete_name, name="complete_name"),
    # Skill URLs
    path("skills/", skill_list, name="skill_list"),
    path("skills/create/", skill_create, name="skill_create"),
    path("skills/<int:pk>/", skill_detail, name="skill_detail"),
    path("skills/<int:pk>/edit/", skill_edit, name="skill_edit"),
    path("skills/<int:pk>/delete/", skill_delete, name="skill_delete"),
    path("my-skills/", my_skills, name="my_skills"),
    # Test URLs
    path("test-404/", lambda request: render(request, "404.html"), name="test_404"),
    path("test-500/", lambda request: render(request, "500.html"), name="test_500"),
    path(
        "simulate-404/",
        lambda request: (_ for _ in ()).throw(Http404("Test 404 error")),
        name="simulate_404",
    ),
]
