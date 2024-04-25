from django.urls import path
<<<<<<< e2dee7c4005701546172ab8b277afe5489b55198
from filtering.views import LoginView,logout_view, rate_view,admin_profile_view,recommendations_view,register_view
# from filtering.views import login

urlpatterns = [
    # path("", MyLogin.as_view()),

    path("login/", LoginView.as_view(),name="login"),
    path("logout/", logout_view,name="logout"),

    path("rate/", rate_view ,name="start"),
    path("adminProfile/", admin_profile_view),
    path("recommendations/", recommendations_view, name="recommendations"),
    path("register/", register_view,)

    


=======
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
>>>>>>> 92af02d6e45f3d636af822f73f7ce3f5df6c029f
]
