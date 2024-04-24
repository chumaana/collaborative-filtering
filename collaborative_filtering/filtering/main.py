import numpy as np
from filtering.algorithms import algorithms
from filtering.models import Book, User


def get_book(queryset):
    filtered_set = set()
    for item in queryset:
        filtered_set.add((item.book))
    return filtered_set


def get_users_reviews():
    users = User.objects.all()
    users_reviews = []
    for user in users:
        user_reviews = user.review.all()
        filtered_reviews = get_book(user_reviews)
        users_reviews.append((user, filtered_reviews))

    return users_reviews


def calculate_similarity(user):
    # print(all_reviews.values_list())
    curr_user_reviews = user.review.all()
    filtered_user_reviews = get_book(
        curr_user_reviews
    )  # only books reviewed by current user
    filtered_all_reviews = get_users_reviews()  # (user, books) reviewed by all users
    comparison = []

    for review in filtered_all_reviews:
        compered_user = review[0]  # user from all users
        if user == compered_user:
            continue
        compere_review = review[1]  # books of that user
        same_books = filtered_user_reviews.intersection(
            compere_review
        )  # set(book) intersection of curr user books and second user
        different_books = compere_review.difference(same_books)
        u1 = []  # array of (book, rate) for current user
        u2 = []  # array of (book, rate) for second user
        for book in same_books:
            u1_review = user.review.get(book=book)
            u1.append((u1_review.book, u1_review.rate))
            u2_review = compered_user.review.get(book=book)
            u2.append((u2_review.book, u2_review.rate))

        # print(f"u1: {u1}, u2: {u2}\n")
        similarity = algorithms.cosine_similarity(u1, u2)
        # print(similarity)
        # print("my rates:", u1, "\n")
        # print("comp_user rates:", u2, "\n")
        # print(f"same books with {compered_user}: {same_books}\n\n")
        # print(f"similarity between {user} and {compered_user} is: {similarity}")

        comparison.append((compered_user, similarity, different_books))

    comparison.sort(key=lambda x: x[1], reverse=True)
    print(comparison)
    return comparison


def calculate_recommendation(comparison):
    all_reviewed_books = []
    for book in Book.objects.all():
        book_reviews = book.review.all()
        if book_reviews:
            all_reviewed_books.append((False, book))
        else:
            print("empty set")

    # for item in comparison:
    #     comp_user = item[0]
    #     similarity = item[1]
    #     diff_books = item[2]
