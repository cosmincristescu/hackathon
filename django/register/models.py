from django.db import models
from passlib.hash import pbkdf2_sha256
# Create your models here.

class Registers(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=255)

	def verify_password(self, raw_password):
		return pbkdf2_sha256.verify(self, raw_password, password)





    
