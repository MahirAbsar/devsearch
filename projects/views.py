from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .utils import paginateProjects
from django.contrib import messages


from users.views import profiles
from .utils import searchProjects
from . models import Project
from .import forms
# Create your views here.

def projects(request):
    projects,search_query = searchProjects(request)
    custom_range,projects=paginateProjects(request,projects,3)
    return render(request,"projects/projects.html",{'projects':projects,'search_query':search_query,'custom_range':custom_range})

def project(request,pk):
    form = forms.ReviewForm()
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            messages.success(request,'Your Review Was Saved Successfully')
            project.getTotalVoteCount
            return redirect('project',pk = project.id)
    return render(request,"projects/single-project.html",{'project':project,'tags':tags,'form':form})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = forms.ProjectForm()
    if request.method == "POST":
        form = forms.ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("projects")
            
    context = {"form":form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url='login')

def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = forms.ProjectForm(instance=project)
    if request.method == "POST":
        form = forms.ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")
            
    context = {"form":form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url='login')

def deleteProject(request,pk):
    profile = request.user.profile
    object = profile.project_set.get(id=pk)
    context ={"object":object}
    if request.method == "POST":
        object.delete()
        return redirect("projects")
    return render(request,'delete_template.html',context)

