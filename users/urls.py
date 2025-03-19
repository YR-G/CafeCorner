from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CafeOwnerViewSet, AdministratorViewSet, register_user, login_user, profile_user, \
    logout_user
from .views import manage_user, update_user, delete_user

app_name = 'users'

# Setting up DefaultRouter for REST API endpoints
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'cafeowners', CafeOwnerViewSet)
router.register(r'administrators', AdministratorViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Includes all router endpoints
    path('register/', register_user, name='register'),  # User registration endpoint
    path('login/', login_user, name='login'),  # User login endpoint
    path('profile/', profile_user, name='profile'),  # User profile endpoint
    path('logout/', logout_user, name='logout'),  # User logout endpoint
    path('manage_user/', manage_user, name='manage_user'),  # User management endpoint
    path('update_user/', update_user, name='update_user'),  # Update user information
    path("delete_user/<int:user_id>/", delete_user, name="delete_user"),  # Delete user endpoint
    path("profile/", profile_user, name="profile"),  # Duplicate profile endpoint (consider removing)
]