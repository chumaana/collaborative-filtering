from django.contrib import admin
from filtering.models import Book, Review, User

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Review)
