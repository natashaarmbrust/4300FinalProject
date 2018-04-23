from __future__ import unicode_literals

from django.db import models

# Create your models here.
# python manage.py makemigrations project_template
# python manage.py migrate

class Docs(models.Model):
	address = models.CharField(max_length=200)

	def __str__(self):
		return self.address
# class Wine(models.Model):
# 	title = models.CharField(max_length=100)
# 	description = models.CharField(max_length=1000)
# 	designation = models.CharField(max_length=50)
# 	points = models.IntegerField
# 	variety = models.CharField(max_length=50)
# 	country = models.CharField(max_length=50)
# 	region = models.CharField(max_length=50)
# 	province = models.CharField(max_length=50)
# 	winery = models.CharField(max_length=50)
# 	price = models.FloatField