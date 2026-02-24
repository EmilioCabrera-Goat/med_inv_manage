from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'
 
	def __str__(self):
		return self.name

class  Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(blank=True, upload_to='photos')
	bio = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Profile of {self.user.username}"