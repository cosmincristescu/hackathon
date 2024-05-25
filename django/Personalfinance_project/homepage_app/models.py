from django.db import models

# Create your models here.
class income(models.Model):
	username_earned = models.CharField(max_length=50)
	what_earned = models.CharField(max_length=50)
	amount_earned = models.FloatField()
	date_earned = models.DateField()
	message_earned = models.TextField()

class expense(models.Model):
	username_expense = models.CharField(max_length=50)
	what_expense = models.CharField(max_length=50)
	amount_expense = models.FloatField()
	date_expense = models.DateField()
	message_expense = models.TextField() 