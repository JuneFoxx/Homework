from django import forms
from .models import Image



class UserForm(forms.Form):
    name = forms.CharField(
        min_length=2,
        max_length=255,
        label="Имя",
        help_text="Ваше имя"
    )
    password = forms.CharField(widget=forms.PasswordInput)
   
    phone = forms.CharField(
        min_length=11, max_length=11, label="Телефон", help_text="Телефон")

    question = forms.CharField(min_length=1, label="Суть вопроса", help_text="Напишите свой вопрос", widget=forms.Textarea)
    
    

class ImageForm(forms.Form):
    url = forms.CharField()
    slug = forms.SlugField()
    
class ImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
    
    
    