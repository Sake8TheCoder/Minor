from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages


def LookUp(request,context):
  return render(request,"LookUp.html",context = context)

def indexPage(request):
  messages.get_messages(request)._loaded_messages.clear()

  if request.method == "POST":
    file1 = request.FILES.get("Image1")
    file2 = request.FILES.get("Image2")
    file3 = request.FILES.get("Image3")
    file4 = request.FILES.get("Image4")
    if not file1 and not file2 and not file3 and not file4:
        messages.info(request,"No file has been entered")
        redirect(indexPage)

    Imgs = {"Images" : [file1 ,file2, file3, file4]}
    return LookUp(request,Imgs)
  
  return render(request,"index.html")


  
