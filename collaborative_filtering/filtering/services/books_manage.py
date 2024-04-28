from django.db.models import Avg, Count
from filtering.models import Book, Review, User


def get_not_rated_books(user):
    user_rated_books_ids = Review.objects.filter(user=user).values_list(
        "book_id", flat=True
    )

    unrated_books = (
        Book.objects.exclude(isbn__in=user_rated_books_ids)
        .annotate(num_reviews=Count("review"), avg_rate=Avg("review__rate"))
        .order_by("-num_reviews", "-avg_rate")[:5]
    )
    # print([book.num_reviews for book in unrated_books])
    return unrated_books


def add_review(user, book, rating):
    if Review.objects.filter(user=user, book=book).exists():
        return "User has already reviewed this book"

    new_review = Review.objects.create(user=user, book=book, rate=rating)
    return new_review
