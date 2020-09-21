from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import  Tables
# Create your views here.
HttpRequest.scheme="http"



def contacts(request):
    return render(request,'mainpage/contacts.html')

def site_info(request):
    return render(request, 'mainpage/site_info.html')

def about(request):
    return render(request,'mainpage/about.html')

def face(request):
    return render(request,'mainpage/test.html')

def net(request):
    tables=Tables.objects.all()
    return render(request,'mainpage/net.html',{'tables':tables})
