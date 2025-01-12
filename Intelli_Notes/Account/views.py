import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import User

@csrf_exempt
def auth_receiver(request):
    token = request.POST.get('credential')

    if not token:
        return HttpResponse("Missing token", status=400)

    print("Received token:", token) 

    try:
        # Verifying the Google token
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        )
    except ValueError:
        return HttpResponse("Invalid Google token", status=403)

    email = user_data.get('email')
    google_id = user_data.get('sub')

    # Check if the user exists by Google ID
    user = User.objects.filter(google_id=google_id).first()

    if user is None:
        # User does not exist, redirect to username setup
        request.session['user_data'] = user_data
        return redirect('set_username')

    # Log the user in if they exist
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    # Update session data after login
    request.session['user_data'] = user_data  # Update user data in session

    # Redirect to the home page after login
    return redirect('home')
@login_required
def set_username(request):
    """
    Prompts the user to set a username if they don't have one yet.
    """
    # Redirect if the user already has a username
    if request.user.username:
        return redirect('home')

    # Handle POST request when the user submits a username
    if request.method == 'POST':
        username = request.POST.get('username')

        # Validate that a username was provided
        if not username:
            return HttpResponse("Please provide a username.", status=400)

        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken. Please try another one.", status=400)

        # Save the new username to the user profile
        user = request.user
        user.username = username
        user.save()

        # Redirect to the home page after saving the username
        return redirect('home')

    # Render the username setup page for a GET request
    return render(request, 'set_username.html')

def sign_in(request):
    """
    Google Sign-In Page
    """
    google_oauth_client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your-google-client-id')
    return render(request, 'sign_in.html', {'google_oauth_client_id': google_oauth_client_id})

def sign_out(request):
    """
    Clears the session and logs the user out.
    """
    request.session.flush()  # Clears the session
    return redirect('sign_in')

def home(request):
    """
    Home Page for Authenticated Users
    """
    user_data = request.session.get('user_data', None)
    if not user_data:
        # Retrieve user data directly from the User model if not in session
        user_data = {
            'given_name': request.user.first_name,
            'email': request.user.email
        }

    return render(request, 'home.html', {'user_data': user_data})