from django.shortcuts import render, redirect
from django.template import RequestContext
import uuid
from django.core.files.storage import default_storage
from django.contrib import messages
import requests
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


def index(request):

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
            "token" : -99,
            "user_email" : -99
        }

    if int(context["user_login"])==1:
        
        return redirect("productSearch:capturecamera")
        
    else:
        return render(request=request, template_name="index.html", context=context)

def capturecamera(request):

    context = isLogin(request)

    if int(context["user_login"]) !=1:

        return redirect("user:login")

    if request.method=="POST":

        if request.POST.get("flexRadioDefault") == "Kadın":

            gender = 1

        else:

            gender = 0

        try:

            file = request.FILES["chooseFile"]
        except:

            messages.info(request, "Lütfen bir dosya seçin veya yükleyin.")
            return redirect("index")
            
        imgId = uuid.uuid1()
        imgId = str(imgId)+".png"

        file_name = default_storage.save(imgId, file)

        request.session["file_name"] = file_name
        
        url = 'https://prediction.hepsitrend.tech:8443/predict/?user_id={}&gender={}'.format(request.session["user_id"],gender)
        files = {'file': open('static/uploads/{}'.format(file_name), 'rb')}
        response = requests.post(url, files=files, auth=BearerAuth(request.session["token"]))

        print(request.session["token"])

        if int(response.status_code) != 200:

            messages.info(request, "İşlem sırasında bir hata oluştu, lütfen tekrar deneyiniz.")

            return render(request, "cameraCapture.html", context)
        
        context["products"] = response.json()

        del context["products"][0]

        context["products"].insert(0, {"pr_id":-99, "img_url":file_name})
        
        return render(request, "view.html", context)
    
    else:

        return render(request, "cameraCapture.html", context)

def view(request):

    pass



class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r