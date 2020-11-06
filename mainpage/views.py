from django.shortcuts import render,redirect
from .models import *
from .forms import TaskForm,CreateUserForm
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import ContributorSerializer, EquipmentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class EquipmentView(APIView):
    def get(self,request, pk=None):
        if pk!=None:
            print("pk is not none")
            equipment = get_object_or_404(Tables.objects.all, pk=pk)
            serializer = EquipmentSerializer(equipment)
            return Response({"equipment": serializer.data})
        else:
            print("pk is none")
            equipment=Tables.objects.all()
            serializer=EquipmentSerializer(equipment, many=True)
            return Response({"equipment":serializer.data})

    #@login_required(login_url='http://127.0.0.1:8000/login/')
    def post(self, request):
        if request.user.is_authenticated==False:
            return Response("you shouldnt access that")
        eq=request.data.get("equipment")
        serializer=EquipmentSerializer(data=eq)
        if serializer.is_valid(raise_exception=True):
            equipment_saved=serializer.save()
            return Response({"success: equipment '{}' added successfully".format(equipment_saved.equip)})

    def put(self, request, pk):
        if request.user.is_authenticated==False:
            return Response("you shouldnt")
        saved_equipment = get_object_or_404(Tables.objects.all(), pk=pk)
        data = request.data.get('equipment')
        serializer = EquipmentSerializer(instance=saved_equipment, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):  # узкое место. добавить else с ответом 400
            saved_equipment = serializer.save()
        return Response({"success": "Contributor '{}' updated successfully".format(saved_equipment.equip)})

    def delete(self, request, pk=None):  # успешно работает
        if request.user.is_authenticated==False:
            return Response("you shouldnt")
        if pk != None:
            # print("pk!=None")
            equipment = get_object_or_404(Tables.objects.all(), pk=pk)
        else:
            # print("pk==None")
            equipment = Tables.objects.all()
        equipment.delete()
        return Response({"message": "Equipment with id '{}' successfully deleted.".format(pk)}, status=204)


class ContribView(APIView):
    def get(self,request, pk=None):
        if pk!=None:
            print("pk not none")
            contributors = get_object_or_404(Contributors.objects.all(), pk=pk)
            serizalizer=ContributorSerializer(contributors)
            return Response({"contributors": serizalizer.data})
        else:
            #print("pk is none")
            contributors = Contributors.objects.all()
            serializer=ContributorSerializer(contributors, many=True)
            return Response({"contributors": serializer.data})

    def post(self,request):
        contributor=request.data.get("contributors")
        serializer=ContributorSerializer(data=contributor)
        if serializer.is_valid(raise_exception=True):
            contributor_saved=serializer.save()
        return Response({"success": "Contributor '{}' added successfully".format(contributor_saved.title)})


    def put(self, request, pk):
        saved_contributor = get_object_or_404(Contributors.objects.all(), pk=pk)
        data = request.data.get('contributors')
        serializer=ContributorSerializer(instance=saved_contributor,data=data,partial=True)

        if serializer.is_valid(raise_exception=True): # узкое место. добавить else с ответом 400
            saved_contributor=serializer.save()
        return Response({"success":"Contributor '{}' updated successfully".format(saved_contributor.title)})

    def delete(self, request, pk=None): # успешно работает
        if pk!=None:
            #print("pk!=None")
            contributor=get_object_or_404(Contributors.objects.all(), pk=pk)
        else:
            #print("pk==None")
            contributor = Contributors.objects.all()
        contributor.delete()
        return Response({"message":"Contributor with id '{}' successfully deleted.".format(pk)}, status=204)


    def head(self,request):
        return Response()


def registerPage(request):
    if request.user.is_authenticated:
        #return redirect('')
        return face(request) #поменять на страничку с сообщением, что разлогинился
        #return loginPage(request)
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                #return redirect('login')
                return loginPage(request)

        context = {'form': form}
        return render(request, 'mainpage/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        #return redirect('')
        return face(request)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                #return redirect('')
                return face(request)
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'mainpage/login.html', context)


def logoutUser(request):
    logout(request)
    #return loginPage(request)
    #return redirect('login')
    return face(request)


def contacts(request):
    return render(request, 'mainpage/contacts.html')


def jspage(request):
    return render(request, 'mainpage/jspage.html',{})


def site_info(request):
    return render(request, 'mainpage/site_info.html')


#def about(request):
#    return render(request, 'mainpage/about.html')


def face(request):
    return render(request, 'mainpage/face.html')#test

def equipment_js(request):
    return render(request, 'mainpage/equipment_page.html')

def net(request):
    if request.method == "GET":
        tabs = Tables.objects.all()
        return render(request, 'mainpage/net.html', {'tables': tabs})
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            print("Форма валидна, сохраняем")
            form.save(commit=True)
        tabs = Tables.objects.all()
        context = {"form": form, "tables": tabs}
        return render(request, 'mainpage/net.html', context)
