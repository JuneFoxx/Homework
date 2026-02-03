from django.db import models

class Poll(models.Model):
    title = models.CharField(verbose_name="Название опроса", blank=False, null=False, unique=True)

class Question(models.Model):
    question = models.CharField(verbose_name="Вопрос", blank=False, null=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name="Название связанного опроса")

class Answer(models.Model):
    option = models.CharField(verbose_name="Вариант", blank=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Название связанного вопроса")
