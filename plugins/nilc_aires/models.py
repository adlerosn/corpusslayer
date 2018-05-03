import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
from django.db import models
import application.models as app_models

# Create your models here.
