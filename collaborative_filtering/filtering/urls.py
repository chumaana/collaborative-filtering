from django.urls import path
from filtering.views import (
    LoginView,
    admin_profile_view,
    logout_view,
    rate_view,
    recommendations_view,
    register_view,
    home_view
)

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("rate/", rate_view, name="start"),
    path("adminProfile/", admin_profile_view),
    path("recommendations/", recommendations_view, name="recommendations"),
    path(
        "register/",
        register_view,
        name="register"
    ),
]
