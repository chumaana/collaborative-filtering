from django.http import HttpResponse
from django.shortcuts import render
from filtering import main


# Create your views here.
def test_core(request):
    print("It is test_core function!")
    reviews = request.user.review.all()
    # print(reviews)
    comparison = main.calculate_similarity(request.user)
    main.calculate_recommendation(comparison)
    context = {"reviews": reviews, "user": request.user}
    return render(request, "index.html", context)
