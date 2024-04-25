from django import forms
from django.contrib.auth.forms import UserCreationForm
from filtering.models import Book, User


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


class MethodChoiceForm(forms.Form):
    CHOICES = [
        ('cosine', 'Cosine similarity'),
        ('pearson', 'Pearson correlation'),
        ('spearman', 'Spearman correlation'),
    ]
    select_field = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    input_books = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter a number'}))
    input_users = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter a number'}))
    input_calc_const = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter a number'}))
