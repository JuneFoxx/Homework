from django.db import models

class Image(models.Model):
    url = models.CharField(verbose_name="Путь к файлу на сервере", blank=False, null=False, unique=True)

class UserAccount(models.Model):
    nickname = models.CharField(verbose_name="Имя пользователя", blank=False, null=False)
    registration_date = models.DateField(verbose_name="Дата регистрации", blank=False, null=False)
    email = models.EmailField(verbose_name="Адрес электронной почты", blank=False, null=False)
    is_admin = models.BooleanField(verbose_name="Является ли администратором", blank=False, null=False, default=False)
    description = models.TextField(verbose_name="О себе")  
