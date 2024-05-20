from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    
    peoples = [{
        "name":"sujan",
        "age" : 24
    },
              {
        "name":"ram",
        "age" : 16
    },
              {
        "name":"sgyam",
        "age" : 20
    },]
    return render(request, "index.html", context={'peoples':peoples})

@login_required(login_url="/login")
def receipes(request):
    if(request.method=="POST"):
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get('receipe_image')
        print(receipe_name, receipe_description)
        print(receipe_image)
        
        Receipe.objects.create(
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image
        )
        return redirect("/receipe/")
    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search') )
        
    context = {'receipes': queryset}
    
    # print(data)
    return render(request, "receipes.html", context)

# ====================================update functionality==========================
def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    
    if(request.method =="POST"):
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get('receipe_image')
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect("/receipe/")
        
    context = {'receipe': queryset}
    return render(request, "update_receipes.html", context)
    

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect("/receipe/")


# ===============================registeration==================================

def register_page(request):
    if(request.method == "POST"):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        isuserExist = User.objects.filter(username = username)
        if isuserExist:
            messages.info(request, "Username alreday exist")
            return redirect("/register")
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Regrestration successful")
        return redirect("/register")
        
    return render(request, "register.html")


# ==============================login page=====================================

def login_page(request):
    if(request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        isuserExist = User.objects.filter(username = username).exists()
        
        if not isuserExist:
            messages.info(request, "INVALID USERNAME ")
            return redirect("/login")
        
        user = authenticate(username=username, password = password)
        
        if user is None:
            messages.error(request, "INVALID PASSWORD ")
            return redirect("/login")
        else:
            print("true")
            login(request, user) 
            return redirect("/receipe/")
              
    return render(request, "login.html")

# =================================logout functionality======================================================

def logout_page(request):
    logout(request)
    return render(request, "login.html")

