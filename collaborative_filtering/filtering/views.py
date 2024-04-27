import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from filtering import main
from filtering.forms import (
    BookReviewForm,
    LoginForm,
    MethodChoiceForm,
    RegisterForm,
    ReviewsFormSet,
)
from filtering.models import Book, User
from filtering.users_books import books_manage


def home_view(request):
    template_name = "filtering/home.html"
    return render(request, template_name)


class LoginView(FormView):
    template_name = "filtering/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("start")

    def form_valid(self, form: LoginForm):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None:
            login(self.request, user)
            if user.is_superuser:
                self.success_url = reverse_lazy("admin_profile") 
            return super().form_valid(form)
        else:
            print("hui")
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)


def logout_view(request):

    logout(request)
    return redirect(reverse_lazy("home"))


def rate_view(request):
    template_name = "filtering/rate.html"

    books = books_manage.get_not_rated_books(request.user)
    if request.method.lower() == "get":
        formset = ReviewsFormSet()
        return render(
            request,
            template_name,
            {"book_forms": zip(books, formset), "formset": formset},
        )

    if request.method.lower() == "post":
        formset = ReviewsFormSet(request.POST)
        formset.full_clean()
        if not formset.is_valid():
            return render(
                request,
                template_name,
                {"book_forms": zip(books, formset), "formset": formset},
            )

        for book, form in zip(books, formset):
            form: BookReviewForm
            print(f"{book=} was rated {form.cleaned_data['like']!r}")
            books_manage.add_review(request.user, book, int(form.cleaned_data["like"]))
        # return render(request, template_name, {'book_forms': zip(books, formset), "formset": formset})
        return redirect(reverse_lazy("recommendations"))


def admin_check(user):
    return user.is_superuser


@user_passes_test(admin_check)
def admin_profile_view(request):
    template_name = "filtering/adminProfile.html"

    if request.method == "POST":
        form = MethodChoiceForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data["select_field"]
            input_books = form.cleaned_data["input_books"]
            input_users = form.cleaned_data["input_users"]
            input_calc_const = form.cleaned_data["input_calc_const"]
            print(selected_option, input_books, input_users, input_calc_const)
            main.process_all_users(
                input_users, input_calc_const, input_books, selected_option
            )
            return render(request, template_name, {"form": form})

    else:
        form = MethodChoiceForm()
        return render(request, template_name, {"form": form})


def recommendations_view(request):
    template_name = "filtering/recommendations.html"

    f = open("recs.json")

    data = json.load(f)
    books = data[str(request.user.id)]
    rec_books = []

    for book in books:
        rec_books.append(Book.objects.get(id=book[0]))
    print("recccc", rec_books)
    f.close()
    return render(request, template_name, {"books": rec_books})

    # return render(request, template_name)


def register_view(request):
    template_name = "filtering/registration.html"

    if request.method == "GET":
        form = RegisterForm()
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("gooooood", form)
            form.save()
            return redirect("login")

    return render(request, template_name, {"form": form})
