import numpy as np
from filtering.models import Book, Review, User


def cosine_similarity(book_ratings1, book_ratings2):
    ratings1 = np.array([rating for _, rating in book_ratings1])
    ratings2 = np.array([rating for _, rating in book_ratings2])

    dot_product = np.dot(ratings1, ratings2)
    norm_ratings1 = np.linalg.norm(ratings1)
    norm_ratings2 = np.linalg.norm(ratings2)

    similarity = dot_product / (norm_ratings1 * norm_ratings2)

    return similarity


def got_users_review_l(username):
    user = User.objects.get(username=username)
    reviews = user.review.all()
    return reviews


def get_book(queryset):
    filtered_set = set()
    for item in queryset:
        filtered_set.add((item.book))
        # print(item.book)
    return filtered_set


def calculate_similarity(user):
    # print(all_reviews.values_list())
    curr_user_reviews = user.review.all()
    filtered_user_reviews = get_book(
        curr_user_reviews
    )  # only books reviewed by current user
    filtered_all_reviews = get_users_reviews()  # (user, books) reviewed by all users

    for review in filtered_all_reviews:
        compered_user = review[0]  # user from all users
        compere_review = review[1]  # books of that user
        same_books = filtered_user_reviews.intersection(
            compere_review
        )  # set(book) intersection of curr user books and second user

        u1 = []  # array of (book rate) for current user
        u2 = []  # array of (book rate) for second user
        for book in same_books:
            u1_review = user.review.get(book=book)
            u1.append((u1_review.book, u1_review.rate))
            u2_review = compered_user.review.get(book=book)
            u2.append((u2_review.book, u2_review.rate))

        similarity = cosine_similarity(u1, u2)
        print(f"similarity between {user} and {compered_user} is: {similarity}")
        # print("my books:", filtered_user_reviews, "\n")
        # print("comp_user books:", compere_review, "\n")
        # print(f"same books with {compered_user}: {same_books}\n\n")


def get_users_reviews():
    all_reviews = Review.objects
    users = User.objects.all()
    users_reviews = []
    for user in users:
        user_reviews = user.review.all()
        filtered_reviews = get_book(user_reviews)
        users_reviews.append((user, filtered_reviews))

    return users_reviews
