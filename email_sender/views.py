from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .script import send_emails
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

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

        # Save the uploaded file
        file_path = default_storage.save('email.xlsx', recipients_file)

        recipients_file_path = default_storage.path(file_path)

        # Send the emails
        result = send_emails(sender_email, sender_password, subject, email_content, recipients_file_path)

        return render(request, 'result.html', {'result': result})

    return render(request, 'send_email.html')
