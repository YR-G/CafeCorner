from django.urls import path
from .views import submit_review
# Define the app namespace for URL routing
app_name = 'reviews'
urlpatterns = [
    path('reviews/<int:cafe_id>/', submit_review, name='get_reviews'),  # Submitting a review for a specific cafe
]
