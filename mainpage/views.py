from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Tables, Contributors
from .forms import TaskForm
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import ContributorSerializer
# Create your views here.


class ContribView(APIView):
    def get(self,request, pk=None):
        if pk!=None:
            #print("pk not none")
            contributors = get_object_or_404(Contributors.objects.all(), pk=pk)
            serizalizer=ContributorSerializer(contributors)
            return Response({"contributors":serizalizer.data})
        else:
            #print("pk is none")
            contributors = Contributors.objects.all()
            serializer=ContributorSerializer(contributors,many=True)
            return Response({"contributors": serializer.data})


    def post(self,request):
        contributor=request.data.get("contributors")
        serializer=ContributorSerializer(data=contributor)
        if serializer.is_valid(raise_exception=True):
            contributor_saved=serializer.save()
        return Response({"success": "Contributor '{}' added successfully".format(contributor_saved.title)})


    def put(self, request, pk):
        saved_contributor = get_object_or_404(Contributors.objects.all(),pk=pk)
        data = request.data.get('contributors')
        serializer=ContributorSerializer(instance=saved_contributor,data=data,partial=True)

        if serializer.is_valid(raise_exception=True):
            saved_contributor=serializer.save()
        return Response({"success":"Contributor '{}' updated successfully".format(saved_contributor.title)})

    def delete(self, request, pk): # успешно работает
        contributor=get_object_or_404(Contributors.objects.all(), pk=pk)
        contributor.delete()
        return Response({"message":"Contributor with id '{}' successfully deleted.".format(pk)}, status=204)

    def head(self,request):
        return Response()


def contacts(request):
    return render(request, 'mainpage/contacts.html')


def site_info(request):
    return render(request, 'mainpage/site_info.html')


def about(request):
    return render(request, 'mainpage/about.html')


def face(request):
    return render(request, 'mainpage/face.html')#test


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
