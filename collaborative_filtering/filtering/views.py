from django.shortcuts import render, redirect

from filtering.forms import RegisterForm,LoginForm
from django.contrib.auth import logout,login,authenticate
from django.views.generic import FormView
from django.urls import reverse_lazy
from filtering import main
from filtering.models import User


class LoginView(FormView):
    template_name = "filtering/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('start')
    
    def form_valid(self, form:LoginForm):  
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None:
            login(self.request, user)    
            return super().form_valid(form)
        else:
            print("hui")
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)


def logout_view(request):
    template_name = "filtering/logout.html"
    render(request,template_name)
    print(request.user)

    logout(request)
    print("out",request.user)

    return redirect(reverse_lazy('login'))
    

def start_user_page_view(request):
    template_name = "filtering/startUserPage.html"
    model=User
    return render(request,template_name)

def admin_profile_view(request):
    template_name = "filtering/adminProfile.html"

    return render(request,template_name)

def recommendations_view(request):
    template_name = "filtering/recommendations.html"

    return render(request,template_name)


def register_view(request):
    template_name = "filtering/registration.html"
    if request.method == 'GET':
        form = RegisterForm()
    return render(request,template_name, {"form": form})
 
         


# Create your views here.
def test_core(request):
    print("It is test_core function!")
    reviews = request.user.review.all()
    # print(reviews)
    comparison = main.calculate_similarity(request.user)
    main.calculate_recommendation(comparison)
    context = {"reviews": reviews, "user": request.user}
    return render(request, "index.html", context)
