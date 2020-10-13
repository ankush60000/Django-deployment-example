from django.shortcuts import render
from user_app.form import Userform,UserProfileInfoform

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login , logout

def index(request):
    return render(request,"user_app/index.html")



@login_required
def special(request):
    return HttpResponse("You Are Logged-IN")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == "POST":
        user_form = Userform(data=request.POST)
        profile_form = UserProfileInfoform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form  = Userform()
        profile_form = UserProfileInfoform()        
    return render(request,'user_app/register.html',
                                                    {'user_form':user_form , 
                                                    'profile_form':profile_form ,
                                                    'registered':registered })






def user_login(request):
    if request.method ==  'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user :
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account IS NOT ACTIVE")
        else:
            print("Someone Try To Login into Your Acount !!!")
            print("username{} and password{}".format(username,password))
            return HttpResponse("invalid login details supplied!!!")
    else:
        return render(request,'user_app/login.html',{})


        