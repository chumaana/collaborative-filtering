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
        user_books = Book.objects.filter(review__user=curr_user)
        if not user_books.exists():
            continue

        user_book_ids = user_books.values_list("isbn", flat=True)
        related_users = (
            users.filter(review__book__in=user_book_ids)
            .distinct()
            .exclude(id=curr_user.id)
        )
        for comp_user in related_users:
            comp_user_books = Book.objects.filter(review__user=comp_user)

            if not comp_user_books.exists():
                continue

            same_books = user_books.intersection(comp_user_books)
            if same_books.count() < min_number_of_books:
                continue

            same_books_ids = same_books.values_list("isbn")
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
            # print(algorithm,similarity)

    with open("similarity.txt", "wb") as f:
        pickle.dump(comparison, f)


def calculate_recommendation(k, users_for_rec) -> dict:
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

        for book in recommend_books.items():
            recommend_books[book[0]] = book[1] + k * get_avg_rate(user)

        recommendations[user.id] = recommend_books

    f.close()
    return recommendations


def process_all_users(users_for_rec, k, min_number_of_books, algorithm="cosine"):
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

    calculate_similarity(algorithm, min_number_of_books)
    recommendations = calculate_recommendation(k, users_for_rec)
    if recommendations:
        with open("recs.txt", "wb") as f:
            pickle.dump(recommendations, f)
