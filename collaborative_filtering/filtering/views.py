from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from filtering import main
from filtering.forms import BookReviewForm, LoginForm, RegisterForm, ReviewsFormSet
from filtering.models import Book, User
from filtering.users_books import books_manage


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
            return super().form_valid(form)
        else:
            print("hui")
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)


def logout_view(request):
    template_name = "filtering/logout.html"
    render(request, template_name)
    print(request.user)

    logout(request)
    print("out", request.user)

    return redirect(reverse_lazy("login"))


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


def admin_profile_view(request):
    template_name = "filtering/adminProfile.html"
    # main.recommend_user(request.user)
    main.process_all_users()
    return render(request, template_name)


def recommendations_view(request):
    template_name = "filtering/recommendations.html"

    return render(request, template_name)


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
