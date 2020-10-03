#from django.contrib import admin
from django.urls import path
from . import views
from .views import ContribView

app_name="about"


urlpatterns = [
    path('', views.face),#главная страница
    #path('about/',views.about), #Про нас
    path('about/', ContribView.as_view()),
    path("about/<int:pk>",ContribView.as_view()),
    path('net/',views.net), #табличка
    path('contacts',views.contacts), #Контакты
    path('site_info',views.site_info)#инфо о сайте
]