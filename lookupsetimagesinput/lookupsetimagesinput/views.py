from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages

def indexPage(request):
  if request.method == "POST":
    pass

  return render(request,"index.html")


  
