from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from account.models import SignUp

def _login(request):
    context = {
        'title': 'Login',
        'error': None,
        'email_invalid_error': None
    }

    if request.user.is_authenticated:
        return redirect('social:index')

    # validate email and password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '' or password == '':
            context['error'] = 'Please fill all fields'
            return render(request, 'accounts/login.html', context=context)

        user = authenticate(username=username, password=password)

        if user is None:
            context['error'] = 'Invalid username or password'
            return render(request, 'accounts/login.html', context=context)


        vdUser = User.objects.filter(username=username).first()
        isValidUser = SignUp.objects.filter(user=vdUser).first()

        if isValidUser and not isValidUser.isValid:
            if vdUser is not None:
                request.session['email'] = vdUser.email
                request.session['signup_id'] = isValidUser.pk
                context['email_invalid_error'] = True
                return render(request, 'accounts/login.html', context=context)

        login(request, user)
        return redirect('studentsapp:form')

    return render(request, 'accounts/login.html', context=context)
