from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Your custom validation logic here
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "userauths/sign-up.html", {'form': UserRegisterForm(request.POST)})

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "userauths/sign-up.html", {'form': UserRegisterForm(request.POST)})

        # If custom validation passes, proceed with creating the user
        new_user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, f"Hey {username}, Your account was created successfully.")
        new_user = authenticate(username=email, password=password1)
        login(request, new_user)
        return redirect("core:index")
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, "userauths/sign-up.html", context)
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey, you are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password") 

        # Validate if email and password are provided
        if not email or not password:
            messages.warning(request, "Please provide both email and password.")
            return render(request, "userauths/sign-in.html")

        # Try to authenticate with email
        user = authenticate(request, username=email, password=password)

        # If email authentication fails, try with username
        if user is None:
            user = authenticate(request, username=email, password=password)

        # Validate if user exists and authentication is successful
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("core:index")
        else:
            messages.warning(request, "It must be email not username and check your password.")

    return render(request, "userauths/sign-in.html", {'messages': messages.get_messages(request)})


        

def logout_view(request):

    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")


def profile_update(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            # Handle the phone field separately to avoid validation error
            new_phone = form.cleaned_data.get('new_phone')
            if not new_phone:
                # If new_phone is not provided, use the existing phone value
                new_phone = profile.phone

            # Update the user's username if provided in the form
            new_username = form.cleaned_data.get('new_username')
            if new_username:
                request.user.username = new_username
                request.user.save()

            # Update profile with new values
            profile.phone = new_phone
            form.save()

            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)


