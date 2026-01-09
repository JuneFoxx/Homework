from django import forms

class UserForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=255, label="Имя", help_text="Ваше имя")
    phone = forms.CharField(min_length=11, max_length=12, label="Телефон", help_text="Ваш телефонный номер")
    password = forms.CharField(widget=forms.PasswordInput)
    question = forms.CharField(min_length=1, label="Суть вашего вопроса", help_text="Напишите свой вопрос", widget=forms.Textarea)

class ImageForm(forms.Form):
    url = forms.CharField()