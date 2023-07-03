from django.shortcuts import render
from django.core.files.storage import default_storage
from .script import send_emails

def send_email_view(request):
    if request.method == 'POST':
        sender_email = request.POST.get('sender_email')
        sender_password = request.POST.get('sender_password')
        subject = request.POST.get('subject')
        email_content = request.POST.get('email_content')
        recipients_file = request.FILES['recipients_file']

        # Save the uploaded file
        file_path = default_storage.save('email.xlsx', recipients_file)

        recipients_file_path = default_storage.path(file_path)

        # Send the emails
        result = send_emails(sender_email, sender_password, subject, email_content, recipients_file_path)

        return render(request, 'result.html', {'result': result})

    return render(request, 'send_email.html')
