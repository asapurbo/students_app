from django.shortcuts import redirect, render
from controllers.account.register_view import register
from controllers.account.email_verify import email_verify
from controllers.account.login_view import _login
from utils.send_to_mail import send_to_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
# this is the register view
# Define a function called register_view that takes in a request as a parameter
def register_view(request):
    if request.user.is_authenticated:
        return redirect('studentsapp:form')
    # Call the register function and pass in the request as an argument
    # views.py
    return register(request)

def verify_email(request):
    if request.user.is_authenticated:
        return redirect('social:index')

    if request.session.get('send_email', None):
        send_to_mail(request)
        request.session['send_email'] = False
    return email_verify(request)


def resend_email(request):
    if request.user.is_authenticated:
        return redirect('social:index')

    request.session['send_email'] = True
    return redirect('account:verify_email')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('social:index')

    return _login(request)


@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')
