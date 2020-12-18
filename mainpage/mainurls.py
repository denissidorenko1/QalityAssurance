from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ContribView, EquipmentView


app_name="about"


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.face),#главная страница
    path('about/', ContribView.as_view()),
    path('about/<int:pk>',ContribView.as_view()),
    path('net/',views.equipment_js), #табличка
    path('contacts/',views.contacts), #Контакты
    path('site_info/',views.site_info), # инфо о сайте
    path('jspage/', views.jspage),
    path('equipment_api/', EquipmentView.as_view()), #rest api link
    path('equipment_api/<int:pk>', EquipmentView.as_view()),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('change_language/', views.change_language, name='change_language'),
    path('routesearcher/', views.routesearcher)

]
