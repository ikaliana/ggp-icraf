from __future__ import unicode_literals

from django.db import models

class BauScenario(models.Model):
	Title = models.CharField(max_length=300)
	Description = models.CharField(max_length=1000)
