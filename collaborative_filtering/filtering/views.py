from django.shortcuts import render, redirect

from filtering.forms import BookReviewForm, ReviewsFormSet, RegisterForm,LoginForm
from django.contrib.auth import logout,login,authenticate
from django.views.generic import FormView
from django.urls import reverse_lazy
from filtering import main
from filtering.models import User,Book
from filtering.users_books import books_manage

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
    
# class StartUserPageView(FormView):
#     template_name = "filtering/startUserPage.html"
#     form_class = ReviewsFormSet

#     def get_context_data(self, **kwargs) -> dict:
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             self.books = Book.objects.exclude(review__user=self.request.user)[:5]
#             context["book_forms"] = zip(self.books, context["form"])
#         return context
#     # success_url = reverse_lazy('start')

#     def form_invalid(self, form):
#        print(f"invalid form {form.__dict__}")
#        for form in form:
#             form: BookReviewForm
#             print(form.cleaned_data, form.is_valid())
#        return super().form_invalid(form) 
    
#     def form_valid(self, form_set:ReviewsFormSet):
#         for book, form in zip(self.books, form_set):
#             form: BookReviewForm
#             print(book, form.cleaned_data, form.is_valid())
#         return super().form_valid(form_set)    
    #     username = form.cleaned_data['username']
    #     password = form.cleaned_data['password']

    #     user = authenticate(self.request, username=username, password=password)
    #     print(user)
    #     if user is not None:
    #         login(self.request, user)    
    #         return super().form_valid(form)
    #     else:
    #         print("hui")
    #         form.add_error(None, "Invalid username or password")
    #         return self.form_invalid(form)


def rate_view(request):
    template_name = "filtering/rate.html"
    
    books = books_manage.get_not_rated_books(request.user)
    if request.method.lower() == "get":
        formset = ReviewsFormSet()
        return render(request, template_name, {'book_forms': zip(books, formset), "formset": formset})
    
    if request.method.lower() == "post":
        formset = ReviewsFormSet(request.POST)
        formset.full_clean()
        if not formset.is_valid():
            return render(request, template_name, {'book_forms': zip(books, formset), "formset": formset})

        for book, form in zip(books, formset):
            form: BookReviewForm
            print(f"{book=} was rated {form.cleaned_data['like']!r}")
            books_manage.add_review(request.user, book,int(form.cleaned_data['like']))
        # return render(request, template_name, {'book_forms': zip(books, formset), "formset": formset})
        return redirect(reverse_lazy('recommendations'))


def admin_profile_view(request):
    template_name = "filtering/adminProfile.html"

    return render(request,template_name)

def recommendations_view(request):
    template_name = "filtering/recommendations.html"
    # print (main.recommend_user(request.user))
    return render(request,template_name)


def register_view(request):
    template_name = "filtering/registration.html"
    
    if request.method == 'GET':
        form = RegisterForm()
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("gooooood",form)
            form.save()
            return redirect('login') 
    
    return render(request, template_name, {"form": form})        


# Create your views here.
# def test_core(request):
#     print("It is test_core function!")
#     reviews = request.user.review.all()
#     # print(reviews)
#     comparison = main.calculate_similarity(request.user)
#     main.calculate_recommendation(comparison)
#     context = {"reviews": reviews, "user": request.user}
#     return render(request, "index.html", context)
