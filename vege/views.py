from django.shortcuts import render, redirect
from .models import *

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
        
    # print(data)
    return render(request, "receipes.html")