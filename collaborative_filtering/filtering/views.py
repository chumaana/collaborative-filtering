from django.http import HttpResponse
from django.shortcuts import render
from filtering import main


# Create your views here.
def test_core(request):
    print("It is test_core function!")
    reviews = main.got_users_review_l(request.user.username)
    # print(reviews)
    main.calculate_similarity(request.user)
    context = {"reviews": reviews, "user": request.user}
    return render(request, "index.html", context)
