import csv

from django.conf import settings
from filtering.models import Book, Review, User


def import_books(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        Book.objects.bulk_create(
            Book(isbn=row["ISBN"], name=row["BookTitle"], author=row["BookAuthor"])
            for row in reader
        )


def import_ratings(file_path):
    out_path = file_path.parent / "reviews.csv"
    # out_path2 = file_path.parent / "reviews2.csv"
    with open(out_path, "r") as f:  # , out_path.open("w") as out:
        reader = csv.DictReader(f)
        # writer = csv.DictWriter(out, reader.fieldnames)
        # writer.writeheader()
        # for row in reader:
        #     if (
        #         int(row["UserID"]) < 10000
        #         and Book.objects.filter(isbn=row["ISBN"]).first()
        #     ):
        #         writer.writerow(row)
        Review.objects.bulk_create(
            Review(book_id=row["ISBN"], rate=row["BookRating"], user_id=row["UserID"])
            for row in reader
        )


def import_users():
    User.objects.bulk_create(
        (
            User(
                username=f"user_{i}",
                password="pbkdf2_sha256$720000$XQnGB89iXIAadiDfhDBlzB$TmCh2nomyEZRYSUWTH/GW4Jm2CAjkntpzolN25IATaw=",
            )
            for i in range(1, 10000)
        )
    )


def main():
    base_path = settings.BASE_DIR / "filtering" / "import"
    book_file_path = base_path / "Books.csv"
    ratings_file_path = base_path / "Ratings.csv"
    users_file_path = base_path / "Users.csv"

    # import_books(book_file_path)
    import_ratings(ratings_file_path)
    # import_users()


main()
