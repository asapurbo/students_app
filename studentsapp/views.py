import uuid
from django.shortcuts import render, redirect
from .models import Student
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import base64
import cloudinary
import cloudinary.uploader
# from cloudinary.utils import cloudinary_url
from decouple import config
# from wkhtmltopdf.views import PDFTemplateResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def form(request):
    context = {
        'error': None,
        'title': 'Form'
    }

    if request.method == 'POST':
        name = request.POST.get('name', None)
        roll = request.POST.get('roll', None)
        session = request.POST.get('session', None)
        comments = request.POST.get('comments', None)
        performance = request.POST.get('performance', None)

        isExist = Student.objects.filter(user=request.user).exists()
        if isExist:
            student = Student.objects.update(name=name, roll=roll, session=session, description=comments, evaluation=int(performance), user=request.user)

            return redirect('studentsapp:signature')

        if not (name and roll and session and comments and performance):
            context['error'] = 'Please fill all the fields'
            return render(request, 'form.html', context)

        student = Student.objects.create(name=name, roll=roll, session=session, description=comments, evaluation=int(performance), user=request.user)
        student.save()
        return redirect('studentsapp:signature')

    return render(request, 'form.html', context=context)


@login_required
def student_pdf(request):
    # Create the HTML content you want to render
    student = Student.objects.filter(user=request.user).first()
    html_content = render_to_string('pdf.html', {'student': student})

    # Convert the HTML content to PDF using WeasyPrint
    pdf = HTML(string=html_content).write_pdf()

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')

    # Set the content disposition header to prompt the browser to download
    response['Content-Disposition'] = 'attachment; filename="downloaded_file.pdf"'

    return response


@login_required
def home(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('studentsapp:form')
    
    return render(request, 'home.html', context={'student': student})


@login_required
def signature(request):
    student = Student.objects.get(user=request.user)
    if student.signature:
        return redirect('studentsapp:home')

    if request.method == 'POST':
        cloudinary.config(
            cloud_name = config('CLOUD_NAME'),
            api_key = config('API_KEY'),
            api_secret = config('API_SECRET'),
            secure=True,
        )

        signature_data = request.POST.get('signature')
        if signature_data:
            # Convert base64 to image
            header, encoded = signature_data.split(",", 1)
            data = base64.b64decode(encoded)

            size = (128, 128)
            upload_result = cloudinary.uploader.upload(
                data,
                folder="signature",
                public_id=uuid.uuid4().hex[:10],
                transformation=[
                    {"width": size[0], "height": size[1], "crop": "auto", "gravity": "auto"},
                    {"fetch_format": "auto", "quality": "auto"}
                ]
            )
            profile_pic = upload_result["secure_url"]

            student = Student.objects.get(user=request.user)
            student.signature = profile_pic
            student.save()
            return redirect('studentsapp:home')

    return render(request, 'signature.html')

