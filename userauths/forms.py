from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    new_username = forms.CharField(max_length=150, required=False, help_text='Leave it empty if you do not want to change your username.')

    class Meta:
        model = Profile
        fields = ['image', 'phone', 'new_username']


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')

            # Assuming you want to update the displayed username after the update
            user.refresh_from_db()
            return render(request, 'edit_profile.html', {'user_profile': user.profile})
            
        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        user_form = UserRegisterForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
