"""collaborative_filtering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from filtering.views import LoginView,logout_view, start_user_page_view,admin_profile_view,recommendations_view,register_view
# from filtering.views import login

urlpatterns = [
    # path("", MyLogin.as_view()),

    path("login/", LoginView.as_view(),name="login"),
    path("logout/", logout_view,name="logout"),

    path("startPage/", start_user_page_view,name="start"),
    path("adminProfile/", admin_profile_view),
    path("recommendations/", recommendations_view),
    path("register/", register_view,)

    


]
