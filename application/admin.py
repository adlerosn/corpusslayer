from django.contrib import admin
from corpusslayer.adminModelRegister import registerForMe
from application import models

# Register your models here.

registerForMe(admin, models)
