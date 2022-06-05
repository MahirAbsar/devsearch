from .import models
from django.forms import ModelForm
from django import forms

class ProjectForm(ModelForm):
 class Meta:
  
  model = models.Project
  fields = ["title",'featured_image',"description","demo_link","source_link","tags"]
  widgets = {
   "tags":forms.CheckboxSelectMultiple()
  }

 def __init__(self,*args,**kwargs):
  super(ProjectForm,self).__init__(*args,**kwargs)
  
  # self.fields['title'].widget.attrs.update({'class':'input',"placeholder":'Add Title'})

  for name , field in self.fields.items():
  
   field.widget.attrs.update({'class':'input','placeholder':'Enter '+name})

class ReviewForm(ModelForm):
 class Meta:
  model = models.Review
  fields = ('value','body')
  labels = {
   'value':'Place you vote',
   'body':'Add a comment with your vote',
  }
 def __init__(self,*args,**kwargs):
  super(ReviewForm,self).__init__(*args,**kwargs) 
  # self.fields['title'].widget.attrs.update({'class':'input',"placeholder":'Add Title'})
  for name , field in self.fields.items():
   field.widget.attrs.update({'class':'input'})