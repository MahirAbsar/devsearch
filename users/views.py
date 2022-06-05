from typing import ContextManager
from django.db.models.query import RawQuerySet
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from users.models import Profile,Message
from .forms import ProfileForm,SkillForm,MessageForm
from .utils import searchProfiles,paginateProfiles
# Create your views here.

def profiles(request):
 
 profiles,search_query = searchProfiles(request)
 custom_range,profiles= paginateProfiles(request,profiles,3)
 return render(request,'users/profiles.html',{"profiles":profiles,'search_query':search_query,
 'custom_range':custom_range})

def userProfile(request,pk):
 profile = Profile.objects.get(id=pk)
 topSkills = profile.skill_set.exclude(description__exact="")
 otherSkills = profile.skill_set.filter(description="")
 return render(request,'users/user-profile.html',{'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills})


def loginPage(request):

 if request.user.is_authenticated:
  return redirect('profiles')

 if (request.method == "POST"):
  username = request.POST.get('username').lower()
  password = request.POST.get('password')
  try:
   user = User.objects.get(username=username)
  except:
   # print("Username Does Not Exist")
   messages.error(request,"Username Does Not Exist")
   return

  user = authenticate(username=username,password=password)
  if user:
   login(request,user)
   return redirect(request.GET['next'] if 'next' in request.GET else 'account')
  else:
   # print("Username Or Password Is Incorrect")  
   messages.error(request,"Username Or Password Is Incorrect")
   

 return render(request,'users/login_register.html',{})

def logoutPage(request):
 logout(request)
 messages.error(request,"User Was Logged Out")
 return redirect('login')

def registerPage(request):
  form = CustomUserCreationForm()
  if request.method=="POST":
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      messages.success(request,"User account was created")
      login(request,user)   
      return redirect('profiles')
    else:
      messages.error(request,"An Error Has Occurred During Registration")
  return render(request,'users/login_register.html',{'page':'register','form':form})

@login_required(login_url="login")
def userAccount(request):
  profile = request.user.profile
  projects = profile.project_set.all()
  skills = profile.skill_set.all()
  context = {"profile":profile,"skills":skills,"projects":projects}
  return render(request,"users/account.html",context)

@login_required(login_url='login')
def editAccount(request):
  form = ProfileForm(instance=request.user.profile)
  if request.method == "POST":
    form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)

    if form.is_valid():
      form.save()
      return redirect('account')

  context = {"form":form}
  return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def addSkills(request):
  profile = request.user.profile
  form = SkillForm()
  if request.method == "POST":
    form = SkillForm(request.POST)
    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner = profile
      skill.save()
      messages.success(request,"Skill Was Added!")
      return redirect('account')

  context = {'form':SkillForm}
  return render(request,'users/skill_form.html',context)

def updateSkills(request,pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id = pk)
  form = SkillForm(instance=skill)
  if request.method == "POST":
    form = SkillForm(request.POST,instance=skill)
    if form.is_valid():
      form.save()
      messages.success(request,"Skill Was Updated!")
      return redirect('account')

  context = {'form':form}
  return render(request,'users/skill_form.html',context)

def deleteSkill(request,pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  if request.method == "POST":
    skill.delete()
    messages.error(request,"Skill Was Updated!")
    return redirect('account')
  
  context ={"object":skill}
  return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    return render(request,'users/inbox.html',context={"messageRequests":messageRequests,"unreadCount":unreadCount})

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        print('Flase')
        message.is_read = True
        message.save()

    return render(request,'users/message.html',context={'message':message})

def createMessage(request,pk):
  receiver = Profile.objects.get(id=pk)
  form = MessageForm()

  try:
    sender = request.user.profile
  except:
    sender = None
  if request.method == "POST":
    form = MessageForm(request.POST)
    if form.is_valid():
      message = form.save(commit=False)
      message.sender = sender
      message.receiver = receiver
      if sender:
        message.name = sender.name
        message.email = sender.email
      message.save()
      messages.success(request,'Message Was Send Successfully!')
      return redirect('user-profile',pk=receiver.id)
  context = {'form':form,'receiver':receiver}
  return render(request,'users/message_form.html',context)

