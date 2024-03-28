from django.http import HttpResponse
from django.shortcuts import render
from filtering.core.main import got_users_review_l


# Create your views here.
def test_core(request):
    print("It is test_core function!")
    reviews = got_users_review_l(request.user.username)
    context = {"reviews": reviews, "user": request.user}
    return render(request, "index.html", context)
