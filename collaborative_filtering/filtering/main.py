import numpy as np
from filtering.algorithms import algorithms
from filtering.models import Book, Review, User


def get_book(queryset) -> set:
    filtered_set = set()
    for item in queryset:
        filtered_set.add((item.book))
    return filtered_set


def get_users_reviews() -> list:
    users = User.objects.all()
    users_reviews = []
    for user in users:
        user_reviews = user.review.all()
        filtered_reviews = get_book(user_reviews)
        users_reviews.append((user, filtered_reviews))

    return users_reviews


def get_avg_rate(user):
    sum_rate = 0
    for review in user.review.all():
        sum_rate += review.rate
    return sum_rate / user.review.count()


def calculate_similarity(user):
    # user_reviewed_books = get_book(
    #     user.review.all()
    # )  # only books reviewed by current user
    user_reviewed_books = set(Book.objects.filter(review__user=user))
    print(user_reviewed_books)
    filtered_all_reviews = get_users_reviews()  # (user, books) reviewed by all users
    comparison = {}

    for review in filtered_all_reviews:
        compered_user = review[0]  # user from all users
        if user == compered_user:
            continue
        compere_books = review[1]  # books of that user
        same_books = user_reviewed_books.intersection(
            compere_books
        )  # set(book) intersection of curr user books and second user
        different_books = compere_books.difference(same_books)

        u1 = []  # array of (book, rate) for current user
        u2 = []  # array of (book, rate) for second user
        if same_books:
            for book in same_books:
                u1_review = user.review.get(book=book)
                u1.append(u1_review.rate)
                u2_review = compered_user.review.get(book=book)
                u2.append(u2_review.rate)

            # print(f"u1: {u1}, u2: {u2}\n")

            cos_similarity = algorithms.cosine_similarity(u1, u2)
            similarity = algorithms.cosine_similarity(u1, u2)
            pear_similarity = algorithms.pearson_correlation(u1, u2)
            spear_similarity = algorithms.spearman_rank_correlation(u1, u2)
            print(f"cos sim with {compered_user} is {cos_similarity}")
            print(f"pear sim with {compered_user} is {pear_similarity}")
            print(f"spear sim with {compered_user} is {spear_similarity}\n")

        comparison[compered_user] = (similarity, different_books)

    # comparison.sort(key=lambda x: x[1], reverse=True)
    # print(comparison)
    return comparison


def calculate_recommendation(comparison, user):
    # check if there are enough users
    user_unread_books_dict = {}

    user_books = set(Book.objects.filter(review__user=user))
    user_unread_books = set(Book.objects.all()).difference(user_books)

    predicted_ratings = {}
    predicted_rate = 0

    for book in user_unread_books:
        book_reviews = Review.objects.filter(book=book)
        if book_reviews:
            for review in book_reviews:
                if review.user == None:
                    continue
                similarity = comparison[review.user][0]
                avg_rate = get_avg_rate(review.user)
                predicted_rate += (review.rate - avg_rate) * similarity

            predicted_ratings[book] = predicted_rate + get_avg_rate(user)

    return predicted_ratings


def recommend_user(user):
    comparison = calculate_similarity(user)
    pred_ratings = calculate_recommendation(comparison, user)

    sorted_books = sorted(pred_ratings.items(), key=lambda item: item[1], reverse=True)
    return sorted_books
