from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.http import Http404
from .views import (
    SignupView,
    home,
    view_my_profile,
    view_user_profile,
    edit_my_profile,
    search,
    complete_name,
    add_skill,
    skills_list_search,
    skill_detail_page,
    skill_edit,
    delete_skill,
    my_skills,
    send_message,
    inbox,
    sent_messages,
    view_message,
    rate_skill,
    css_test,
)


def redirect_to_home(request):
    return redirect("home")


urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home_alt"),
    path("index/", redirect_to_home, name="index_redirect"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="core/auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="core/auth/logout.html", next_page=None
        ),
        name="logout",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("search/", search, name="search"),
    path("profile/", view_my_profile, name="view_my_profile"),
    path("profile/<int:user_id>/", view_user_profile, name="view_user_profile"),
    path("profile/edit/", edit_my_profile, name="edit_my_profile"),
    path("profile/complete-name/", complete_name, name="complete_name"),
    # Skill URLs
    path("skills/", skills_list_search, name="skills_list_search"),
    path("skills/create/", add_skill, name="add_skill"),
    path("skills/<int:pk>/", skill_detail_page, name="skill_detail_page"),
    path("skills/<int:pk>/edit/", skill_edit, name="skill_edit"),
    path("skills/<int:pk>/delete/", delete_skill, name="delete_skill"),
    path("my-skills/", my_skills, name="my_skills"),
    # Messaging URLs
    path("skills/<int:skill_id>/message/", send_message, name="send_message"),
    path("message/<int:user_id>/", send_message, name="send_message_to_user"),
    path("inbox/", inbox, name="inbox"),
    path("sent/", sent_messages, name="sent_messages"),
    path("messages/<int:message_id>/", view_message, name="view_message"),
    # Rating URLs
    path("skills/<int:skill_id>/rate/", rate_skill, name="rate_skill"),
    # CSS Test URL
    path("css-test/", css_test, name="css_test"),
    # Test URLs
    path("test-404/", lambda request: render(request, "404.html"), name="test_404"),
    path("test-500/", lambda request: render(request, "500.html"), name="test_500"),
    path(
        "simulate-404/",
        lambda request: (_ for _ in ()).throw(Http404("Test 404 error")),
        name="simulate_404",
    ),
]
