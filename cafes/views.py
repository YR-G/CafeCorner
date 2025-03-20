import re
import cloudinary
from django.contrib import messages
from django.db.models import Count, OuterRef, Subquery
from django.views.decorators.csrf import csrf_exempt
from reviews.models import Review
from users.models import CafeOwner
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from cafes.models import CafeShop

def homepage(request):
    # Retrieve the top 3 cafes based on their average rating in descending order
    cafes = CafeShop.objects.all()
    for cafe in cafes:
        cafe.update_average_rating()
    top_cafes = CafeShop.objects.order_by('-average_rating')[:3]
    # Render the homepage template with the top cafes data
    return render(request, "homepage.html", {"top_cafes": top_cafes})


from django.shortcuts import render, redirect


def information(request):
    # Check if the user is logged in and is a cafe owner
    if "user_id" not in request.session or request.session.get("user_type") != "cafe_owner":
        return redirect("users:login")

    # Get the user ID from the session
    user_id = request.session["user_id"]
    # Retrieve the cafe owned by the user, or create a new one if not found
    cafe = CafeShop.objects.filter(owner_id=user_id).first()

    if not cafe:
        cafe = CafeShop(owner_id=user_id)

    # Retrieve the cafe owner details
    owner = CafeOwner.objects.filter(id=user_id).first()

    # Handle form submission for updating cafe information
    if request.method == "POST":
        cafe.name = request.POST.get("name", cafe.name)
        cafe.introduction = request.POST.get("introduction", cafe.introduction)
        cafe.address = request.POST.get("address", cafe.address)
        cafe.price_range = request.POST.get("price_range", cafe.price_range)
        cafe.contact = request.POST.get("contact", cafe.contact)

        # Check if an image file is uploaded and store it using Cloudinary
        if "img" in request.FILES:
            uploaded_image = cloudinary.uploader.upload(request.FILES["img"])
            cafe.img_url = uploaded_image["secure_url"]

        # Attempt to save the updated cafe information
        try:
            cafe.save()
            messages.success(request, "Cafe information updated successfully!")
        except Exception as e:
            print("Error Saving Cafe Information:", e)
            messages.error(request, "Error saving cafe information.")

        # Additional attempt to save the cafe information
        try:
            cafe.save()
        except Exception as e:
            print("Error Saving Cafe Information:", e)

        # Redirect to the cafe information page after saving
        return redirect("cafes:information")

    # Render the information page with cafe and owner details
    return render(request, "information.html", {"cafe": cafe, "owner": owner})


def cafe_management(request):
    # Retrieve the search query from the request, default to an empty string if not provided
    search_query = request.GET.get('search', '')
    # Filter cafes based on the search query, performing a case-insensitive search on the cafe name
    if search_query:
        cafes = CafeShop.objects.filter(name__icontains=search_query)
    else:
        # If no search query is provided, retrieve all cafes
        cafes = CafeShop.objects.all()

    # Render the cafe management page with the list of cafes
    return render(request, 'manage_cafe.html', {'cafes': cafes})


# Regular expression pattern for validating UK postcodes
POSTCODE_REGEX = r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$"
# Disable CSRF protection for this view (not recommended for production)
@csrf_exempt
def update_cafe(request):
    # Ensure the request method is POST
    if request.method == "POST":
        # Retrieve the cafe ID from the request data
        cafe_id = request.POST.get("id")
        # Get the cafe object, or return a 404 error if not found
        cafe = get_object_or_404(CafeShop, id=cafe_id)

        # Retrieve and validate the address input, converting it to uppercase
        address = request.POST.get("address", "").strip().upper()
        if not re.match(POSTCODE_REGEX, address):
            return JsonResponse({"status": "error", "message": "Invalid postcode format! Please enter a valid UK postcode."})

        # Update cafe details with the new data
        cafe.name = request.POST.get("name")
        cafe.address = address
        cafe.owner.email = request.POST.get("email")
        cafe.price_range = request.POST.get("price_range")
        # Save the updated cafe information
        cafe.save()
        # Return a success response in JSON format
        return JsonResponse({"status": "success", "message": "Cafe details updated successfully!"})
    # Return an error response if the request method is not POST
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def delete_cafe(request, cafe_id):
    # Ensure the request method is DELETE
    if request.method == "DELETE":
        # Retrieve the cafe object by ID, or return a 404 error if not found
        cafe = get_object_or_404(CafeShop, id=cafe_id)
        # Delete the cafe from the database
        cafe.delete()
        # Return a success response in JSON format
        return JsonResponse({"status": "success", "message": "Café deleted successfully!"})
    # Return an error response if the request method is not DELETE
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def cafe_overview(request, cafe_id):
    try:
        # Retrieve the cafe object by ID
        cafe = CafeShop.objects.get(id=cafe_id)
        cafe.update_average_rating()
        # Retrieve all reviews for the cafe, ordered by most recent first
        reviews = Review.objects.filter(cafe=cafe).order_by('-id')
    except CafeShop.DoesNotExist:
        # If the cafe does not exist, set cafe and reviews to None
        cafe = None
        reviews = None
    # Render the overview page with cafe details and associated reviews
    return render(request, "overview.html", {"cafe": cafe, "reviews": reviews})


@csrf_exempt
def upload_cafe_image(request):
    # Check if the request method is POST and an image file is uploaded
    if request.method == "POST" and request.FILES.get("img"):
        uploaded_file = request.FILES["img"]
        try:
            # Upload the image to Cloudinary
            result = cloudinary.uploader.upload(uploaded_file)
            image_url = result.get("secure_url")

            # Retrieve the cafe associated with the logged-in user
            cafe = CafeShop.objects.get(owner=request.session["user_id"])
            # Update the cafe's image URL
            cafe.img = image_url
            cafe.save()
            # Return a success response with the uploaded image URL
            return JsonResponse({"status": "success", "img_url": image_url})
        except Exception as e:
            # Return an error response if an exception occurs
            return JsonResponse({"status": "error", "message": str(e)})
    # Return an error response if the request is not valid
    return JsonResponse({"status": "error", "message": "Invalid request"})
# Print Cloudinary configuration details for debugging
print("Cloudinary Config:", cloudinary.config().cloud_name)


def write_review(request, cafe_id):
    # Check if the user is logged in by verifying if "user_id" exists in the session
    if "user_id" not in request.session:
        # Redirect the user to the login page with a "next" parameter to return to the review page after login
        login_url = f"/users/login/?next=/review/{cafe_id}/"
        return redirect(login_url)
    # Retrieve the cafe object by its ID, or return a 404 error if not found
    cafe = get_object_or_404(CafeShop, id=cafe_id)
    # Render the review page with the cafe details
    return render(request, "review.html", {"cafe": cafe})


def search_cafe(request):
    # Retrieve the search query from the request and remove leading/trailing spaces
    query = request.GET.get("query", "").strip()
    # If the query is empty, return a JSON response indicating an empty query
    if not query:
        return JsonResponse({"success": False, "message": "Empty query"}, status=200)

    try:
        # Attempt to find a cafe with an exact name match (case-insensitive)
        cafe = CafeShop.objects.get(name__iexact=query)
        # Return a JSON response with the matching cafe's ID
        return JsonResponse({"success": True, "cafe_id": cafe.id}, status=200)
    except CafeShop.DoesNotExist:
        # If no matching cafe is found, return a JSON response indicating no results
        return JsonResponse({"success": False, "message": "No matching cafe"}, status=200)


def sorting(request):
    # Retrieve filter and order preferences from request parameters, with default values
    filter_by = request.GET.get("filter", "rating")
    order_by = request.GET.get("order", "high-to-low")
    review_count_subquery = Review.objects.filter(cafe_id=OuterRef('id')).annotate(
        count=Count('id')
    ).values('count')[:1]

    # Annotate cafes with the number of reviews
    cafes = CafeShop.objects.annotate(reviews_count=Subquery(review_count_subquery))

    # Define the sorting field based on the filter parameter
    sort_field = {
        "rating": "average_rating",
        "reviews": "reviews_count",
        "price": "price_range"
    }.get(filter_by, "average_rating")   # Default to sorting by average rating

    # Apply sorting order (ascending or descending)
    if order_by == "low-to-high":
        cafes = cafes.order_by(sort_field)
    else:
        cafes = cafes.order_by(f"-{sort_field}")

    # Create a list of cafe details for JSON response or rendering
    cafe_list = [
        {
            "id": cafe.id,
            "name": cafe.name,
            "average_rating": str(cafe.average_rating),
            "reviews_count": cafe.reviews_count,
            "price_range": cafe.price_range,
            "address": cafe.address,
            "description": cafe.introduction if cafe.introduction else "",
            "img_url": cafe.img_url if cafe.img_url else "/static/image/default.jpg"
        }
        for cafe in cafes
    ]

    # If the request is an AJAX request, return JSON response with cafe details
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        cafe_list = [
            {
                "id": cafe.id,
                "name": cafe.name,
                "average_rating": str(cafe.average_rating),
                "reviews_count": cafe.reviews_count,
                "price_range": cafe.price_range,
                "address": cafe.address,
                "description": cafe.introduction if cafe.introduction else "",
                "img_url": cafe.img_url if cafe.img_url else "/static/image/default.jpg"
            }
            for cafe in cafes
        ]
        return JsonResponse(cafe_list, safe=False)
    # Render the sorting page with the sorted cafe data
    return render(request, "sorting.html", {"cafes": cafes})