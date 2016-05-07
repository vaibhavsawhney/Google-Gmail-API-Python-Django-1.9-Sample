import pickle
import base64

from django.contrib import admin
#from django.contrib.auth.models import User
from django.db import models

from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField

class User(models.Model):
	username=models.CharField(max_length=200,primary_key=True)
	firstname=models.CharField(max_length=20)
	lastname=models.CharField(max_length=20)
	email = models.EmailField()

	def __str__(self):
		return self.username


class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass


