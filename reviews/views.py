from functools import wraps
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from reviews.models import CafeShop, Review
from users.models import Customer


def session_login_required(view_func):
    """
        Decorator to enforce user login based on session data.

        This decorator checks if the "user_id" key exists in the session.
        If the user is not logged in, they are redirected to the login page,
        with a "next" parameter to return to the originally requested page after login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if "user_id" is present in the session
        if "user_id" not in request.session:
            # Redirect to the login page with the original request path as the "next" parameter
            return redirect(f"/users/login/?next={request.path}")
        # Proceed with the original view function if the user is logged in
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@session_login_required
def submit_review(request, cafe_id):
    """
        Handles the submission of a review for a specific cafe.

        - If the user is not logged in, they are redirected to the login page.
        - If the request method is POST, a new review is created for the cafe.
        - The average rating of the cafe is updated after submission.
        - If the request method is not POST, the review page is rendered with the review count.
    """
    # Check if the user is logged in; if not, redirect to the login page
    if "user_id" not in request.session:
        return redirect(f"/users/login/?next=/review/{cafe_id}/")

    # Retrieve the cafe object by its ID, or return a 404 error if not found
    cafe = get_object_or_404(CafeShop, id=cafe_id)
    # Retrieve the logged-in customer based on session user ID
    user_id = request.session["user_id"]
    customer = get_object_or_404(Customer, id=user_id)
    # If the request is a POST request, process the review submission
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        # Create a new review record in the database
        Review.objects.create(
            customer=customer,
            cafe=cafe,
            rating=rating,
            comment=comment
        )

        # Recalculate and update the cafe's average rating
        cafe.average_rating = Review.objects.filter(cafe=cafe).aggregate(Avg("rating"))["rating__avg"] or 0.0
        cafe.save()
        # Redirect to the cafe overview page after submitting the review
        return redirect(reverse("cafes:cafe_overview", kwargs={"cafe_id": cafe.id}))
    # Get the total number of reviews for the cafe
    reviews_count = Review.objects.filter(cafe=cafe).count()
    # Render the review submission page with cafe details and review count
    return render(request, "review.html", {"cafe": cafe, "reviews_count": reviews_count})




