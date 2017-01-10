from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Code(models.Model):
	code = models.CharField(max_length=100000)
	time = models.DateTimeField(auto_now=True)
