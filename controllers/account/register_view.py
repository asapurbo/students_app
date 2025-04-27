import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from account.models import SignUp
from utils import send_to_mail
from django.db.models import Q

# from cloudinary.utils import cloudinary_url
from decouple import config

def register(request):
    context = {
        'title': 'Sign Up',
        'error': None
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm_password']

        # if username and password and email and password and confirm_password:
        if not (username and password and email and password and confirm_password):
            context['error'] = 'Please fill all the fields'
            return render(request, 'accounts/signup.html', context=context)

        # if password != confirm_password
        if password != confirm_password:
            context['error'] = 'Password does not match'
            return render(request, 'accounts/signup.html', context=context)

        # user has been exists
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            context['error'] = 'User already exists'
            return render(request, 'accounts/signup.html', context=context)

        # email validation
        try:
            validate_email(email)
        except ValidationError:
            context['error'] = 'Invalid email'
            return render(request, 'accounts/signup.html', context=context)

        # create user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # create Sign-up data
        signup_data = SignUp.objects.create(user=user)
        signup_data.save()

        # save session
        request.session['email'] = email
        request.session['signup_id'] = signup_data.pk
        send_to_mail.send_to_mail(request)

        return redirect('account:verify_email')

    return render(request, 'accounts/signup.html', context=context)
