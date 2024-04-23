from django.shortcuts import render, redirect
from django.contrib.auth.models import  User
from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Try to retrieve the user object using the provided email
            user = User.objects.get(email=username) #this will rtturn username
            # print(user.first_name)
            # print(username)
        except User.DoesNotExist:
            user = None
        
        # If user object exists, attempt to authenticate using email and password
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
        
        # If authentication with email fails or user object doesn't exist, try with username
        if user is None:
            user = authenticate(request, username=username, password=password)
        
        # If user is authenticated, log them in
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            error_message = "Invalid Credentials"
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        firstname=request.POST.get('firstName')
        lastname=request.POST.get('lastName')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        repasswowrd=request.POST.get('confirmPassword')
        terms = request.POST.getlist('terms')
        
        if password!=repasswowrd:
            error_message = "Passwords do not match"
            return render(request, 'register.html', {'error_message': error_message})
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save() 
        return redirect('login')
    return render(request,'register.html')

def home(request):
    return render(request,'home.html')

def forgot_password(request):
    return render(request, 'send_code.html')

def terms_and_conditons(request):
    return render(request , 'terms.html')

def landing(request):
    return render(request, 'landing.html')

def send_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        if not User.objects.filter(email=email).exists():
            error_message = "Email does not exist"
            return render(request, 'send_code.html', {'error_message': error_message})
        else:
            code = get_random_string(length=6)  # Generate a random 6-character code
            request.session['verification_code'] = code
            email_body = render_to_string('email_template.txt', {'code': code})
            send_mail(
                'Verification code',
                email_body,
                'sachinkoirala9999@gmail.com',
                [email],
                fail_silently=False
                )
    return render(request, 'enter_code.html', {'email': email})
   

def enter_code(request):
    if request.method == 'POST':
        code=request.POST.get('code')
        email=request.session.get('email')
        stored_code = request.session.get('verification_code')
        if code == stored_code:
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                error_message = "Passwords do not match"
                return render(request, 'enter_code.html', {'error_message': error_message})
            else:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            email = request.POST.get('email')
            error_message = "Invalid verification code"
            return render(request, 'enter_code.html', {'email': email, 'error_message': error_message})
    else:
        # Render the enter code page
        return render(request, 'enter_code.html')