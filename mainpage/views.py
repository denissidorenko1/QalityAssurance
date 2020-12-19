from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import TaskForm, CreateUserForm
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import ContributorSerializer, EquipmentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from TRSIS_lab_1 import settings
from mainpage import traversal

mainjs= """
var app=angular.module('app',[])

var postJson=function(link,$http,title,bio,id)
{
    var request=$http({
        method:"post",
        url: link,
        //transformRequest:
        data:
            {
            "contributors": {
        "title": title,
        "bio": bio,
        "contributor_id": id
    }
}

    })
    console.log("post")
}


var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

app.controller('MainCtrl', function($scope, $http)
    {
        $scope.title_input="Дефолтное ФИО"
        $scope.bio_input="Дефолтное БИО"
        $scope.contributor_id_input=0
        $scope.GetC = function ()
        {
            getJSON('https://trsis-labs.azurewebsites.net/about/', function(err, data) {
            if (err !== null)
            {
                 alert('Something went wrong: ' + err);
            }
            else {
                console.log(data["contributors"])
                $scope.val=data["contributors"]
                }
            });

        }

        $scope.Post=function ()
        {
            postJson('https://trsis-labs.azurewebsites.net/about/',$http, $scope.title_input,$scope.bio_input, $scope.contributor_id_input);
            console.log("tried posting")
        }

        $scope.DeleteAll=function ()
        {
            $http.delete('https://trsis-labs.azurewebsites.net/about/')
        }
    }
)
"""

def shit_to_int(N):
    for i in range(len(N)):
        for j in range(len(N)):
            if N[i][j] is None:
                N[i][j] = 0
            else:
                N[i][j] = 1
    return N

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

    # @login_required(login_url='http://127.0.0.1:8000/login/')
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
            print("pk!=None")
            equipment = get_object_or_404(Tables.objects.all(), pk=pk)
        else:
            print("pk==None")
            equipment = Tables.objects.all()
        equipment.delete()
        return Response({"message": "Equipment with id '{}' successfully deleted.".format(pk)}, status=204)

#
class ContribView(APIView):
    def get(self,request, pk=None):
        if pk!=None:
            print("pk not none")
            contributors = get_object_or_404(Contributors.objects.all(), pk=pk)
            serizalizer=ContributorSerializer(contributors)
            return Response({"contributors": serizalizer.data})
        else:
            print("pk is none")
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
            print("pk!=None")
            contributor=get_object_or_404(Contributors.objects.all(), pk=pk)
        else:
            print("pk==None")
            contributor = Contributors.objects.all()
        contributor.delete()
        return Response({"message":"Contributor with id '{}' successfully deleted.".format(pk)}, status=204)


    def head(self,request):
        return Response("200")




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


def mainjslol(request):
    return HttpResponse(mainjs)


def contacts(request):
    #return HttpResponse(mainjs)
    return render(request, 'mainpage/contacts.html')


def jspage(request):
    return render(request, 'mainpage/jspage.html',{})


def site_info(request):
    return render(request, 'mainpage/site_info.html')

@csrf_exempt
def routesearcher(request):
    if request.method == 'POST':
        #do shit
        x00 = request.POST.get('x00')
        x01 = request.POST.get('x01')
        print(x01)
        x02 = request.POST.get('x02')
        x03 = request.POST.get('x03')
        x04 = request.POST.get('x04')
        x05 = request.POST.get('x05')
        x06 = request.POST.get('x06')
        x07 = request.POST.get('x07')
        x08 = request.POST.get('x08')
        x09 = request.POST.get('x09')

        x10 = request.POST.get('x10')
        x11 = request.POST.get('x11')
        x12 = request.POST.get('x12')
        x13 = request.POST.get('x13')
        x14 = request.POST.get('x14')
        x15 = request.POST.get('x15')
        x16 = request.POST.get('x16')
        x17 = request.POST.get('x17')
        x18 = request.POST.get('x18')
        x19 = request.POST.get('x19')

        x20 = request.POST.get('x20')
        x21 = request.POST.get('x21')
        x22 = request.POST.get('x22')
        x23 = request.POST.get('x23')
        x24 = request.POST.get('x24')
        x25 = request.POST.get('x25')
        x26 = request.POST.get('x26')
        x27 = request.POST.get('x27')
        x28 = request.POST.get('x28')
        x29 = request.POST.get('x29')

        x30 = request.POST.get('x30')
        x31 = request.POST.get('x31')
        x32 = request.POST.get('x32')
        x33 = request.POST.get('x33')
        x34 = request.POST.get('x34')
        x35 = request.POST.get('x35')
        x36 = request.POST.get('x36')
        x37 = request.POST.get('x37')
        x38 = request.POST.get('x38')
        x39 = request.POST.get('x39')

        x40 = request.POST.get('x40')
        x41 = request.POST.get('x41')
        x42 = request.POST.get('x42')
        x43 = request.POST.get('x43')
        x44 = request.POST.get('x44')
        x45 = request.POST.get('x45')
        x46 = request.POST.get('x46')
        x47 = request.POST.get('x47')
        x48 = request.POST.get('x48')
        x49 = request.POST.get('x49')

        x50 = request.POST.get('x50')
        x51 = request.POST.get('x51')
        x52 = request.POST.get('x52')
        x53 = request.POST.get('x53')
        x54 = request.POST.get('x54')
        x55 = request.POST.get('x55')
        x56 = request.POST.get('x56')
        x57 = request.POST.get('x57')
        x58 = request.POST.get('x58')
        x59 = request.POST.get('x59')

        x60 = request.POST.get('x60')
        x61 = request.POST.get('x61')
        x62 = request.POST.get('x62')
        x63 = request.POST.get('x63')
        x64 = request.POST.get('x64')
        x65 = request.POST.get('x65')
        x66 = request.POST.get('x66')
        x67 = request.POST.get('x67')
        x68 = request.POST.get('x68')
        x69 = request.POST.get('x69')

        x70 = request.POST.get('x70')
        x71 = request.POST.get('x71')
        x72 = request.POST.get('x72')
        x73 = request.POST.get('x73')
        x74 = request.POST.get('x74')
        x75 = request.POST.get('x75')
        x76 = request.POST.get('x76')
        x77 = request.POST.get('x77')
        x78 = request.POST.get('x78')
        x79 = request.POST.get('x79')

        x80 = request.POST.get('x80')
        x81 = request.POST.get('x81')
        x82 = request.POST.get('x82')
        x83 = request.POST.get('x83')
        x84 = request.POST.get('x84')
        x85 = request.POST.get('x85')
        x86 = request.POST.get('x86')
        x87 = request.POST.get('x87')
        x88 = request.POST.get('x88')
        x89 = request.POST.get('x89')

        x90 = request.POST.get('x90')
        x91 = request.POST.get('x91')
        x92 = request.POST.get('x92')
        x93 = request.POST.get('x93')
        x94 = request.POST.get('x94')
        x95 = request.POST.get('x95')
        x96 = request.POST.get('x96')
        x97 = request.POST.get('x97')
        x98 = request.POST.get('x98')
        x99 = request.POST.get('x99')

        N= [
            [x00, x01, x02, x03, x04, x05, x06, x07, x08, x09],
            [x10, x11, x12, x13, x14, x15, x16, x17, x18, x19],
            [x20, x21, x22, x23, x24, x25, x26, x27, x28, x29],
            [x30, x31, x32, x33, x34, x35, x36, x37, x38, x39],
            [x40, x41, x42, x43, x44, x45, x46, x47, x48, x49],
            [x50, x51, x52, x53, x54, x55, x56, x57, x58, x59],
            [x60, x61, x62, x63, x64, x65, x66, x67, x68, x69],
            [x70, x71, x72, x73, x74, x75, x76, x77, x78, x79],
            [x80, x81, x82, x83, x84, x85, x86, x87, x88, x89],
            [x90, x91, x92, x93, x94, x95, x96, x97, x98, x99],
        ]
        a=int(request.POST.get('a_node'))
        b=int(request.POST.get('b_node'))
        N=shit_to_int(N)
        path=traversal.traversal_wrapper(N, a, b)
        pathlol=""
        if path is not False:
            for i in range(len(path)):
                pathlol += str(path[i]) + " "
        else:
            pathlol = "Пути нет"
        #pathlol="0 1 "
        print(pathlol)
        #return HttpResponse(path)
        return render(request, 'mainpage/QA_lab.html', {'pathlol': pathlol})
    else:
        return render(request, 'mainpage/QA_lab.html')
#def about(request):
#    return render(request, 'mainpage/about.html')


def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


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
