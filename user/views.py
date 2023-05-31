from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, UpdateUser
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import requests
from requests.auth import HTTPBasicAuth

# Create your views here.

def isLogin(request):

    try:
        context = {
            "user_login" : request.session["login"],
            "user_id" : request.session["user_id"],
            "token" : request.session["token"],
            "user_email" : -99
        }

    except:

        context = {
            "user_login" : -99,
            "user_id" : -99,
            "user_token" : -99,
            "user_email" : -99
        }

    return context

def registerUser(request):

    context = isLogin(request)

    if int(context["user_login"]) == 1:

        return redirect("index")

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data.get("username")
        user_surname = form.cleaned_data.get("user_surname")
        user_email = form.cleaned_data.get("user_email")
        user_phone = form.cleaned_data.get("user_phone")
        erken_erisim = form.cleaned_data.get("erken_erisim")
        password = form.cleaned_data.get("password")

        url = 'https://users.hepsitrend.tech:2053/user/register'

        dictt = {"user_name" : username,
                 "user_surname" : user_surname,
                 "user_email" : user_email,
                 "user_phone" : user_phone,
                 "user_password" : password,
                 "user_code" : erken_erisim
                 
        }

        response = requests.post(url, json = dictt)

        if int(response.status_code) != 201:

            messages.warning(request, str(response.text))

        else:
            
            messages.success(request, str(response.text))

        return redirect("index")
    
    else:

        context["form"] = form

        return render(request, "register.html", context=context)

def loginUser(request):

    context = isLogin(request)

    if int(context["user_login"]) == 1:

        return redirect("index")
    
    form = LoginForm(request.POST or None)

    context["form"] = form

    if form.is_valid():

        user_email = form.cleaned_data.get("user_email")
        password = form.cleaned_data.get("password")

        url = 'https://users.hepsitrend.tech:2053/user/login'
        dictt = {"user_email" : user_email,
                 "user_password" : password}

        response = requests.post(url, json = dictt)

        if int(response.status_code) != 200:
            messages.info(request, "Kullanıcı adı veya parola hatalı")
            return render(request, "login.html", context=context)

        else:

            jsonRes = response.json()["access_token"]
            user_id = response.json()["user_id"]

            request.session["login"] = 1
            request.session["token"] = str(jsonRes)
            request.session["user_id"] = user_id

            messages.success(request, "Giriş Başarılı")

            return redirect("index")
    else:
        return render(request, "login.html", context=context)

def logoutUser(request):

    context = isLogin(request)

    if int(context["user_login"]) != 1:

        return redirect("index")

    request.session["login"] = -99
    request.session["token"] = -99
    request.session["user_id"] = -99
    request.session["user_email"] = -99

    messages.success(request, "Çıkş işlemi başarılı")

    return redirect("index")


def my(request):

    context = isLogin(request)

    if int(context["user_login"]) != 1:

        return redirect("user:login")
    
    form = UpdateUser(request.POST or None)

    if form.is_valid():


        if int(request.POST.get("account"))==1:

            password = form.cleaned_data.get("password")

            dictt = {"user_email" : request.session["user_email"],
                     "user_password" : password
            }

            response = requests.delete('https://users.hepsitrend.tech:2053/user/', json = dictt, auth=BearerAuth(request.session["token"]))
            

            if int(response.status_code) == 202:

                request.session["login"] = -99
                request.session["token"] = -99
                request.session["user_id"] = -99
                request.session["user_email"] = -99

                messages.info(request, "Hesabınız devre dışı bırakılmıştır.")

                return redirect("index")
            
            else:

                request.session["login"] = -99
                request.session["token"] = -99
                request.session["user_id"] = -99
                request.session["user_email"] = -99

                messages.info(request, "Hatalı şifre, çıkış işlemi gerçekleştirildi.")

                return redirect("index")

        username = form.cleaned_data.get("username")
        user_surname = form.cleaned_data.get("user_surname")
        #user_email = form.cleaned_data.get("user_email")
        password = form.cleaned_data.get("password")


        dictt = {"user_email" : request.session["user_email"],
                 "user_name" : username,
                 "user_surname" : user_surname,
                 "user_password" : password
        }

        response = requests.put('https://users.hepsitrend.tech:2053/user/', json = dictt, auth=BearerAuth(request.session["token"]))
            
        if int(response.status_code) == 202:

            messages.success(request, response.text)
            return redirect("user:my")
        
        else:

            messages.info(request, response.text)
            
            request.session["login"] = -99
            request.session["token"] = -99
            request.session["user_id"] = -99
            request.session["user_email"] = -99

            return redirect("index")


    else:

        
        getUrl = 'https://users.hepsitrend.tech:2053/user/getUser/{}'.format(request.session["token"])

        response = requests.get(getUrl, auth=BearerAuth(request.session["token"]))
        
        if int(response.status_code) != 200:

            request.session["login"] = -99
            request.session["token"] = -99
            request.session["user_id"] = -99
            request.session["user_email"] = -99

            messages.success(request, "Çıkş işlemi gerçekleştirildi")

            return redirect("index")
        
        else:

            jsonRespons = response.json()

            form.fields["username"].initial = jsonRespons["user_name"]
            form.fields["user_surname"].initial = jsonRespons["user_surname"]
            form.fields["user_email"].initial = jsonRespons["user_email"]
            form.fields["user_phone"].initial = jsonRespons["user_phone"]

            request.session["user_email"] = jsonRespons["user_email"]

            context["form"] = form

            return render(request, "my.html", context=context)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
    
