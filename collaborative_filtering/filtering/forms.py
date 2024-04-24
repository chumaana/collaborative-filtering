from django import forms
from django.contrib.auth.forms import UserCreationForm
from filtering.models import User, Book


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class BookReviewForm(forms.Form):
    CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]
    like = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
    )

ReviewsFormSet = forms.formset_factory(BookReviewForm, extra=5)