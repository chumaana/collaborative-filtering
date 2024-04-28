import os
import pickle
from bisect import insort

import numpy as np
from filtering.models import Book, Review, User
from filtering.services import algorithms

ALGORITHMS = {
    "cosine": algorithms.cosine_similarity,
    "pearson": algorithms.pearson_correlation,
    "spearman": algorithms.spearman_rank_correlation,
}


def get_avg_rate(user):
    sum_rate = 0
    for review in user.review.all():
        sum_rate += review.rate
    return sum_rate / user.review.count()


def calculate_similarity(algorithm, min_number_of_books) -> None:
    comparison = {}
    min_number_of_books = int(min_number_of_books)
    users = User.objects.all()
    for curr_user in users:
        similarities = []
        # print(f"Calculating for user {curr_user}")
        user_books = Book.objects.filter(review__user=curr_user)
        # print(f"My {curr_user} books: {user_books}")
        if not user_books.exists():
            # print(f"No books")
            continue

        user_book_ids = user_books.values_list("isbn", flat=True)
        related_users = (
            users.filter(review__book__in=user_book_ids)
            .distinct()
            .exclude(id=curr_user.id)
        )
        # print(f"{related_users=} for {curr_user=}")
        for comp_user in related_users:
            comp_user_books = Book.objects.filter(review__user=comp_user)
            # print(f"{comp_user=} books: {comp_user_books}")
            if not comp_user_books.exists():
                continue

            same_books = user_books.intersection(comp_user_books)
            if same_books.count() < min_number_of_books:
                # print(f"not enough, got {same_books.count()}")
                continue
            # print(f"Same books: {same_books}")

            same_books_ids = same_books.values_list("isbn")
            # print(same_books2)
            curr_rates = (
                Review.objects.filter(user=curr_user, book__in=same_books_ids)
                .order_by("book_id")
                .values_list("rate", flat=True)
            )
            comp_rates = (
                Review.objects.filter(user=comp_user, book__in=same_books_ids)
                .order_by("book_id")
                .values_list("rate", flat=True)
            )
            # print(f"Comparing {curr_user.username} and {comp_user.username}")

            if ALGORITHMS.get(algorithm):
                similarity = ALGORITHMS[algorithm](curr_rates, comp_rates)
                if not np.isnan(similarity):
                    insort(
                        similarities,
                        (comp_user, similarity),
                        key=lambda item: -1 * item[1],
                    )

        if len(similarities):
            comparison[curr_user] = similarities

    with open("similarity.txt", "wb") as f:
        pickle.dump(comparison, f)


def calculate_recommendation(user, k, users_for_rec) -> dict:
    users = User.objects.all()

    f = open("similarity.txt", "rb")
    comparison = pickle.load(f)
    recommendations = {}

    for user in users:
        if user not in comparison:
            continue

        recommend_books = dict()
        user_books_ids = Book.objects.filter(review__user=user).values_list(
            "isbn", flat=True
        )
        user_unread_books = Book.objects.exclude(isbn__in=user_books_ids)

        if users_for_rec > len(comparison[user]):
            users_for_rec = len(comparison[user])

        users_to_recommend = comparison[user][:users_for_rec]

        for user_item in users_to_recommend:
            similarity = user_item[1]
            rec_user = user_item[0]

            proccess_books_ids = Book.objects.filter(
                isbn__in=rec_user.review.values_list("book_id", flat=True)
            ).intersection(user_unread_books)

            for book in proccess_books_ids:
                review = rec_user.review.get(book_id=book.isbn)
                avg_rate = get_avg_rate(rec_user)
                predicted_rate = (review.rate - avg_rate) * similarity
                recommend_books[book] = recommend_books.get(book, 0) + predicted_rate

        # print(recommend_books)
        for book in recommend_books.items():
            recommend_books[book[0]] = book[1] + k * get_avg_rate(user)

        recommendations[user.id] = recommend_books

        # books_to_proccess.update(proccess_books)

        #     for review in Review.objects.filter(
        #         book_id__in=proccess_books.values_list("isbn")
        #     ):
        #         avg_rate = get_avg_rate(rec_user)
        #         predicted_rate += (review.rate - avg_rate) * similarity

        # predicted_ratings[book.isbn] = predicted_rate + k * get_avg_rate(user)

        # for book in user_unread_books:
        #     book_reviews = book.review.all()
        #     if book_reviews:
        #         for review in book_reviews:
        #             if review.user in sliced_comparison:
        #                 similarity = sliced_comparison[review.user][0]
        #                 avg_rate = get_avg_rate(review.user)
        #                 predicted_rate += (review.rate - avg_rate) * similarity

        #         predicted_ratings[book.isbn] = predicted_rate + k * get_avg_rate(user)
    f.close()
    return recommendations


def process_all_users(user, users_for_rec, k, min_number_of_books, algorithm="cosine"):
    if min_number_of_books is None:
        min_number_of_books = 1
    else:
        min_number_of_books = int(min_number_of_books)
    if k is None:
        k = 0.5
    else:
        k = float(k)
    if users_for_rec is None:
        users_for_rec = 1
    else:
        users_for_rec = int(users_for_rec)

    # data = {}
    # similarity = {}
    calculate_similarity(algorithm, min_number_of_books)
    # with open("similarity.txt", "rb") as f:
    #     similarity = pickle.load(f)
    # for key in similarity:
    # print(f"{key}: related_users: {similarity[key]}\n")

    recommendations = calculate_recommendation(user, k, users_for_rec)
    if recommendations:
        with open("recs.txt", "wb") as f:
            pickle.dump(recommendations, f)

    # if os.stat("recs.txt").st_size != 0:
    #     with open("recs.txt", "rb") as f:
    #         recs = pickle.load(f)

    # print(f"Recs length: {len(recs)}; Simil length: {len(similarity)}")

    # for key in recs:
    #     print(f"Rec {key}: {recs[key]}")

    # for key in similarity:
    #     print(f"Sim {key}")
