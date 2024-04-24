
from filtering.models import Book, User,Review



def get_not_rated_books(user):
    user_rated_books_ids = Review.objects.filter(user=user).values_list('book_id', flat=True)

    unrated_books = Book.objects.exclude(id__in=user_rated_books_ids)[:5]
    return unrated_books

def add_review(user, book, rating):
    if Review.objects.filter(user=user, book=book).exists():
        return "User has already reviewed this book"

    new_review = Review.objects.create(user=user, book=book, rate=rating)


    return new_review