from django.urls import path
from .views import homepage, information, delete_cafe, update_cafe, cafe_management, cafe_overview, \
    upload_cafe_image, sorting, write_review, search_cafe
# Define the app namespace for URL routing
app_name = "cafes"
urlpatterns = [
    path('', homepage, name='homepage'),
    path("sorting/", sorting, name="sorting"),  # Sorting cafes based on different criteria
    path("information/", information, name="information"),
    path('manage_cafe/', cafe_management, name='manage_cafe'),
    path('update_cafe/', update_cafe, name='update_cafe'),
    path('delete_cafe/<int:cafe_id>/', delete_cafe, name="delete_cafe"),  # Deleting a specific cafe
    path('overview/<int:cafe_id>/', cafe_overview, name='cafe_overview'),  # Displaying cafe details and reviews
    path('upload_cafe_image/', upload_cafe_image, name='upload_cafe_image'),
    path("review/<int:cafe_id>/", write_review, name="write_review"),  # Submitting a review for a cafe
    path("search/", search_cafe, name="search_cafe"),  # Searching for a cafe by name


]
