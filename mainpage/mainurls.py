#from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.face),#главная страница
    path('about',views.about), #Про нас
    path('net',views.net), #табличка
    path('contacts',views.contacts), #Контакты
    path('site_info',views.site_info)#инфо о сайте
]