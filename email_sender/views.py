from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UploadedFile  # Add the UploadedFile import
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .script import send_emails

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('send_email')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('send_email')
    else:
        form = CustomAuthenticationForm(request=request)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login view after logout

@login_required
@csrf_protect
def send_email_view(request):
    if request.method == 'POST':
        sender_email = request.POST.get('sender_email')
        sender_password = request.POST.get('sender_password')
        subject = request.POST.get('subject')
        email_content = request.POST.get('email_content')
        recipients_file = request.FILES['recipients_file']

        # Create a new instance of UploadedFile
        uploaded_file = UploadedFile(uploaded_by=request.user, file=recipients_file)
        uploaded_file.save()

        recipients_file_path = uploaded_file.file.path

        # Send the emails
        result = send_emails(sender_email, sender_password, subject, email_content, recipients_file_path)

        return render(request, 'result.html', {'result': result})

    return render(request, 'send_email.html')
