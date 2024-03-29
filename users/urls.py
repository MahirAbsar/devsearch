from django.urls import path
from . import views

urlpatterns = [

 path('register/',views.registerPage,name="register"),
 path('login/',views.loginPage,name="login"),
 path('logout/',views.logoutPage,name="logout"),

 path('',views.profiles,name="profiles"),
 path('profile/<str:pk>',views.userProfile,name="user-profile"),
 path('account/',views.userAccount,name="account"),
 path('edit-account/',views.editAccount,name="edit-account"),
 path('add-skill',views.addSkills,name="add-skill"),
 path('update-skill/<str:pk>',views.updateSkills,name="update-skill"),
 path('delete-skill/<str:pk>',views.deleteSkill,name="delete-skill"),
 path('inbox/',views.inbox,name="inbox"),
 path('message/<str:pk>',views.viewMessage,name="message"),
 path('create-message/<str:pk>',views.createMessage,name="create-message")

 
]