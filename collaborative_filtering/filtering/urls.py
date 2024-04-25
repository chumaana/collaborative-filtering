from django.urls import path
from filtering.views import (
    MyLogin,
    admin_profile_view,
    recommendations_view,
    register_view,
    start_user_page_view,
)

# from filtering.views import login

urlpatterns = [
    path("login/", MyLogin.as_view()),
    path("startPage/", start_user_page_view),
    path("adminProfile/", admin_profile_view),
    path("recommendations/", recommendations_view),
    path(
        "register/",
        register_view,
    ),
]
