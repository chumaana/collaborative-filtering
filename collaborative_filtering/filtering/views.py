from django.shortcuts import render

# # Create your views here.
# def login(request):
#     # return render(request, "filtering/login.html")

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


class MyLogin(LoginView):
    redirect_authenticated_user = True
    template_name = "filtering/login.html"

    
    def get_success_url(self):
        return reverse_lazy('tasks') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

def start_user_page_view(request):
    template_name = "filtering/startUserPage.html"

    return render(request,template_name)

def admin_profile_view(request):
    template_name = "filtering/adminProfile.html"

    return render(request,template_name)

def recomendations_view(request):
    template_name = "filtering/recomendations.html"

    return render(request,template_name)