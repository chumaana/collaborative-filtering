from filtering import models

# from django.contrib.auth import get_user_model


# def got_users_review(request):
#     loged_user = request.user
#     print()
#     reviewed_books = loged_user.review
    

def got_users_review_l(username):
    user = models.User.objects.get(username=username)
    print(user)


got_users_review_l("user_local1")
