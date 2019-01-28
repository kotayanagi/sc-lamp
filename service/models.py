import json

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    account = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100, verbose_name="title")
    title_link = models.CharField(max_length=100, verbose_name="title_link", null=True)
    date_title = models.CharField(max_length=100, verbose_name="date_title", null=True)
    keyword = models.CharField(max_length=30, verbose_name="keyword", null=True, blank=True)
    keyword_link = models.CharField(max_length=100, verbose_name="keyword_link", null=True, blank=True)
    