from django.shortcuts import redirect, render
from account.models import SignUp

def email_verify(request):
    context = {
        'title': 'Email Verification',
        'error': None,
        'self_email': request.session.get('email', None),
    }

    if(not (request.session.get('otp', None) and request.session.get('email', None))):
        return redirect('account:login')

    if request.method == 'POST':
        otp = request.POST.get('otp', None)

        if not (otp == request.session.get('otp', None)):
            context['error'] = 'OTP is not valid'
            return render(request, 'accounts/email_verify.html', context=context)

        SignUp.objects.filter(id=request.session.get('signup_id', None)).update(isValid=True)
        return redirect('account:login')


    return render(request, 'accounts/email_verify.html', context=context)

