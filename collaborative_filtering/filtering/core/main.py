from filtering.models import User


def got_users_review_l(username):
    user = User.objects.get(username=username)
    reviews = user.review.all()
    return reviews
