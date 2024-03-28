from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=64)


class User(AbstractUser):
    REQUIRED_FIELDS = []


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self) -> str:
        return f"Review: user-{self.user.username}, book-{self.book.name}, rate-{self.rate}"
