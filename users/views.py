from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Customer, CafeOwner, Administrator
from .serializers import CustomerSerializer, CafeOwnerSerializer, AdministratorSerializer
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# ViewSet for Customer model
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# ViewSet for CafeOwner model
class CafeOwnerViewSet(viewsets.ModelViewSet):
    queryset = CafeOwner.objects.all()
    serializer_class = CafeOwnerSerializer

# ViewSet for Administrator model
class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


# Function to handle user registration
def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user_type = request.POST.get("user_type")  # Either 'customer' or 'owner'

        # Validate if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("users:register")

        # Check if email is already registered
        if Customer.objects.filter(email=email).exists() or CafeOwner.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("users:register")

        # Create user based on the user type
        if user_type == "customer":
            user = Customer(first_name=first_name, last_name=last_name, email=email, password=make_password(password))
        else:
            user = CafeOwner(first_name=first_name, last_name=last_name, email=email, password=make_password(password))

        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect("users:login")  # Redirect to login page after registration

    return render(request, "register.html")


# Function to handle user login
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "/")

        user = None
        user_type = None

        # Identify the user type
        if Customer.objects.filter(email=email).exists():
            user = Customer.objects.get(email=email)
            user_type = "customer"
        elif CafeOwner.objects.filter(email=email).exists():
            user = CafeOwner.objects.get(email=email)
            user_type = "cafe_owner"
        elif Administrator.objects.filter(email=email).exists():
            user = Administrator.objects.get(email=email)
            user_type = "admin"

        # Validate user credentials
        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["username"] = user.first_name
            request.session["user_type"] = user_type

            messages.success(request, "Login successful!")

            # Redirect based on user type
            if user_type == "admin":
                return redirect("users:manage_user")
            elif user_type == "cafe_owner":
                return redirect("cafes:information")
            elif user_type == "customer":
                return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")


# Function to handle user logout
def logout_user(request):
    request.session.flush()
    list(messages.get_messages(request))
    messages.success(request, "You have been logged out.")
    return redirect("users:login")


# Function to update user information
@csrf_exempt
def update_user(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        identity = request.POST.get("identity")

        # Identify user type and get user object
        if identity == "Customer":
            user = get_object_or_404(Customer, id=user_id)
        elif identity == "Cafe Owner":
            user = get_object_or_404(CafeOwner, id=user_id)
        else:
            return JsonResponse({"status": "error", "message": "Invalid user identity."})

        # Update user details
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        return JsonResponse({"status": "success", "message": "User details updated successfully!"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})


# Function to delete user
@csrf_exempt
def delete_user(request, user_id):
    if request.method == "DELETE":
        try:
            user = Customer.objects.filter(id=user_id).first()
            if not user:
                user = CafeOwner.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({"status": "error", "message": "User not found"}, status=404)
            user.delete()
            return JsonResponse({"status": "success", "message": "User deleted successfully"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# Function to manage users
def manage_user(request):
    query = request.GET.get("search", "").strip()

    # Retrieve all Customers and CafeOwners
    customers = Customer.objects.all()
    cafe_owners = CafeOwner.objects.all()

    # Filter users based on search query
    if query:
        customers = customers.filter(email__icontains=query)
        cafe_owners = cafe_owners.filter(email__icontains=query)

    users = list(customers) + list(cafe_owners)

    # Assign identity label to each user
    for user in users:
        user.identity = "Customer" if isinstance(user, Customer) else "Cafe Owner"

    return render(request, "manage_user.html", {"users": users})


# Function to display and update user profile
def profile_user(request):
    if "user_id" not in request.session:
        return JsonResponse({"status": "error", "message": "User not logged in"}, status=403)

    user_id = request.session["user_id"]
    user_type = request.session["user_type"]

    user = Customer.objects.get(id=user_id) if user_type == "customer" else CafeOwner.objects.get(id=user_id)

    if request.method == "POST":
        import json
        data = json.loads(request.body)  # Parse JSON request data

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        password = data.get("password", "").strip()

        # Update user information
        if first_name:
            user.first_name = first_name
            request.session["username"] = first_name
        if last_name:
            user.last_name = last_name
        if password:
            user.password = make_password(password)
        user.save()
        return JsonResponse({"status": "success", "message": "Profile updated successfully!"})

    return render(request, "profile.html", {"user": user})
