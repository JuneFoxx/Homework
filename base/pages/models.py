from django.db import models


class Image(models.Model):
    url = models.CharField(verbose_name="Путь к файлу на сервере", blank=False, null=False)
    slug = models.SlugField(blank=True, default=None, null=True, unique=True)
