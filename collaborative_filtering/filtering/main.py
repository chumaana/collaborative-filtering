import json

from filtering.algorithms import algorithms
from filtering.models import Book, Review, User


class UserBooks:
    def __init__(self, user, books):
        self.user = user
        self.books = books


ALGORITHMS = {
    "cosine": algorithms.cosine_similarity,
    "pearson": algorithms.pearson_correlation,
    "spearman": algorithms.spearman_rank_correlation,
}


def get_users_reviews() -> list[UserBooks]:
    users = User.objects.all()
    users_and_books = []
    for user in users:
        user_books = set(Book.objects.filter(review__user=user))
        users_and_books.append(UserBooks(user, user_books))

    return users_and_books


def get_avg_rate(user):
    sum_rate = 0
    for review in user.review.all():
        sum_rate += review.rate
    return sum_rate / user.review.count()


def calculate_similarity(
    user, user_books, algorithm, min_number_of_books
) -> dict | None:
    # print(user_reviewed_books)
    users_and_their_books = get_users_reviews()  # (user, books) reviewed by all users
    comparison = {}

    for user_and_books in users_and_their_books:
        # print(user_and_books.user, user_and_books.books)
        compered_user = user_and_books.user  # user from all users
        if user == compered_user:
            continue
        compare_books = user_and_books.books  # books of that user
        if not len(compare_books):
            continue

        same_books = user_books.intersection(
            compare_books
        )  # set(book) intersection of curr user books and second user
        if len(same_books) < min_number_of_books:
            continue

        different_books = compare_books.difference(same_books)

        u1 = []  # array of (book, rate) for current user
        u2 = []  # array of (book, rate) for second user
        for book in same_books:
            u1_review = user.review.get(book=book)
            u1.append(u1_review.rate)
            u2_review = compered_user.review.get(book=book)
            u2.append(u2_review.rate)

        # cos_similarity = algorithms.cosine_similarity(u1, u2)
        if ALGORITHMS[algorithm]:
            similarity = ALGORITHMS[algorithm](u1, u2)
            if similarity != False:
                comparison[compered_user] = (similarity, different_books)
            else:
                continue

    # comparison.sort(key=lambda x: x[1], reverse=True)
    {
        k: v
        for k, v in sorted(comparison.items(), key=lambda item: item[1], reverse=True)
    }
    print("comparison:", comparison)
    return comparison


def calculate_recommendation(comparison, user, user_books, k, users_for_rec) -> dict:
    user_unread_books = set(Book.objects.all()).difference(user_books)
    if users_for_rec > len(comparison):
        users_for_rec = len(comparison)

    predicted_ratings = {}
    predicted_rate = 0

    # slice = slice(users_for_rec)
    # users_to_include = comparison[slice]

    # print(f"USER: {user}")
    # print(f"Books user has read: {user_books}")
    # print(f"Books user has NOT read: {user_unread_books}")
    for book in user_unread_books:
        book_reviews = book.review.all()
        if book_reviews:
            # print(f"{book} reviews: {book_reviews}")
            for review in book_reviews:
                if review.user in comparison:
                    similarity = comparison[review.user][0]
                    avg_rate = get_avg_rate(review.user)
                    predicted_rate += (review.rate - avg_rate) * similarity

            predicted_ratings[book.id] = predicted_rate + k * get_avg_rate(user)
            # print(predicted_ratings)

    # print("\n")
    return predicted_ratings


def recommend_user(user, users_for_rec, k, min_number_of_books, algorithm):
    user_books = set(Book.objects.filter(review__user=user))
    if not len(user_books):
        print(f"{user} doesn't have reviewed books")
        return None

    comparison = calculate_similarity(user, user_books, algorithm, min_number_of_books)
    # print(comparison)
    pred_ratings = calculate_recommendation(
        comparison, user, user_books, k, users_for_rec
    )

    sorted_books = sorted(pred_ratings.items(), key=lambda item: item[1], reverse=True)
    return sorted_books


def process_all_users(users_for_rec, k, min_number_of_books, algorithm="cosine"):
    if min_number_of_books is None:
        min_number_of_books = 1
    if k is None:
        k = 0.5
    if users_for_rec is None:
        users_for_rec = 1

    data = {}
    for user in User.objects.all():
        recommendations = recommend_user(
            user, users_for_rec, k, min_number_of_books, algorithm
        )
        data[user.id] = recommendations

    with open("recs.json", "w") as f:
        json.dump(data, f)
