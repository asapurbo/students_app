from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from utils.generate_otp import generate_otp

def send_to_mail(request):
    # send email
    email = request.session.get('email')
    otpId = generate_otp()
    request.session['otp'] = otpId
    request.session.set_expiry(300)
    subject = 'Email Verification!'

    message = f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Email</title>
            </head>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">

            <div style="max-width: 600px; margin: 40px auto; background-color: #f4f4f4; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                <h2 style="text-align: center; color: #333333; font-size: 24px; margin-bottom: 20px;">🔐 Your One-Time Password (OTP)</h2>

                <p style="text-align: center; color: #666666; font-size: 16px; margin-bottom: 20px;">
                Use the OTP below to complete your login. It’s valid for 5 minutes.
                </p>

                <div style="font-size: 30px; font-family: 'Courier New', monospace; background-color: #f0f0f0; padding: 15px; color: #333333; border-radius: 8px; text-align: center; letter-spacing: 5px; margin-bottom: 20px;">
                {otpId}
                </div>

                <p style="text-align: center; color: #999999; font-size: 14px;">
                If you didn’t request this, you can safely ignore this email.
                </p>

                <div style="text-align: center; margin-top: 30px; color: #bbbbbb; font-size: 12px;">
                &copy; 2025 Your Company. All rights reserved.
                </div>
            </div>

        </body>
        </html>
    """

    email_msg = EmailMultiAlternatives(
        subject=subject,
        body="Your OTP is below",  # fallback plain text version
        from_email=settings.EMAIL_HOST_USER,
        to=[email]
    )

    email_msg.attach_alternative(message, "text/html")
    email_msg.send(fail_silently=False)
