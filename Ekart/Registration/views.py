from django.shortcuts import render
from Registration.forms import UserForm,UserProfileInfoForm
from shop.models import Order
from Registration.models import UserProfileInfo,UserOTP
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import random

def profileinfo(request,uname):
    user_current = User.objects.filter(username = uname)
    profile_user_current = UserProfileInfo.objects.filter(user = user_current[0])
    orders = Order.objects.all()
    print("length of orders")
    print(len(orders))
    return render(request,"Registration/profile.html",{'useractive':profile_user_current[0],'orders':orders})

def register(request):
    registered = False
    if request.method == 'POST':
        user_input = request.POST.get('user','')
        if user_input:
            otp = request.POST.get('otp','')
            user_input = User.objects.filter(username=user_input)[0]
            if otp:
                if( otp == (UserOTP.objects.filter(user = user_input).last()).otp):
                    user_input.is_active = True
                    user_input.save()
                    login(request, user_input)
                    messages.success(request,"Your account has been verified")
                    return HttpResponseRedirect(reverse('index'))
                else:
                    messages.error(request,"OTP mismatched")
                    return render(request,'Registration/Register.html',{'otp':True,'user':user_input})
            else:
                otp = genOTP()
                print(otp)
                UserOTP.objects.create(user=user_input, otp=otp)
                message = "Your OTP for Account - Validation is" + str(otp)
                send_mail(
                    'Validate your E-mail',
                    message,
                    'muskanbansal581@gmial.com',
                    [user_input.email],
                    fail_silently=False,
                )
                messages.success(request,"OTP Resent!")
                return render(request,'Registration/Register.html',{'otp':True,'user':user_input})
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)
        curr_user = request.POST.get('username','')
        user_existing = User.objects.filter(username = curr_user)
        if(len(user_existing)) and user_existing[0].is_active == False:
            user_existing[0].delete()
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            otp = genOTP()
            UserOTP.objects.create(user=user,otp=otp)
            message = "Your OTP for Account - Validation is" + str(otp)
            html_message = "<html><body><a href = 'http://www.facebook.com'>Click to Reset</a></body></html>"
            send_mail(
                'Validate your E-mail',
                message,
                'muskanbansal581@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )
            print("muskan")
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            print("Saved")
            registered = True
            print(otp)
            return render(request,'Registration/Register.html',{'otp':True,'user':user})
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'Registration/Register.html',
            {'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                print(user.username)
                #next = request.POST.get('next', '/../')
                #return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("User not active")
        else:
            return HttpResponse("Invalid Login Details")

    return render(request,"Registration/login.html")

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email','')
        user = User.objects.filter(email = email)[0]
        current_site = get_current_site(request)
        message = "Click on the link below to Reset your password"
        email_contents = {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':PasswordResetTokenGenerator().make_token(user),
        }
        link = reverse('change_password',kwargs={'uidb64':email_contents['uid'],'token':email_contents['token']})
        activate_url = 'http://'+current_site.domain+link
        html_message = "<html><body><a href='"+ activate_url+"'>Reset Password</a></body></html>"
        send_mail('Password Reset',
                  message,
                  'muskanbansal581@gmail.com',
                  [email],
                  html_message=html_message)
        print(email)
        return HttpResponse("The link to reset your password has been sent to your mail")
    return render(request,"Registration/forget_password.html")

def change_password(request,uidb64,token):
        if request.method == "POST":
            new_password = request.POST.get('new_password','')
            confirm_new_password = request.POST.get('confirm_new_password''')
            if new_password == confirm_new_password:
                user_id = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
                user.set_password(new_password)
                user.save()
                print(new_password)
                print(user.password)
                print("WILL RUN SECOND")
                return HttpResponse('Password Reset successfull')
            else:
                return render(request,"Registration/change_password.html")
        else:
            print("WILL RUN FIRST")
            return render(request,"Registration/change_password.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def genOTP():
    return (random.randint(100000,999999));