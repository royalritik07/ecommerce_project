from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
# SignUp
from django.views.generic import View
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
# Login
from django.contrib.auth import authenticate, login, logout
# Create your views here.


# Resister of SignUp
def signup(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password :
            messages.error(request, "Password is not matching")
            return render(request, 'signup.html')
        
        if User.objects.filter(email = email).exists():
            messages.warning(request, "Username already exists")
            return render(request, 'signup.html')

        user_obj = User.objects.create(
            email=email
        )
        user_obj.set_password(password)
        print(user_obj)
        user_obj.is_active = False
        user_obj.save()
        email_subject = "Activate your account"
        message = render_to_string('activate.html',{
            'user_obj' : user_obj,
            'domain':'127.0.0.1:8000',
            'uid' : urlsafe_base64_encode(force_bytes(user_obj.pk)),
            'token' : generate_token.make_token(user_obj)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(request, "Activate Your Account by clicking on the link in your gmail")
        return redirect('/auth/login/')
    

    return render(request, 'signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try: 
            uid = force_str(urlsafe_base64_decode(uidb64))
            user_obj = User.objects.get(pk=uid)
            
        except Exception as identifier:
            user_obj = None

        if user_obj is not None and generate_token.check_token(user_obj, token):
            user_obj.is_active = True
            user_obj.save()

            messages.info(request, "Account Created Successfully")
            return redirect('/auth/login/')
        
        return render(request, 'activatefail.html')


# Login
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print("Email : ", email)
        print("Password : ",password)

        if not User.objects.filter(email = email).exists():
            messages.warning(request, 'Email do not exists')
            return redirect('/auth/login/')
        
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Password')
            return redirect('/auth/login/')
            

    return render(request, 'login.html')



def logout_page(request):
    return redirect('/auth/login/')