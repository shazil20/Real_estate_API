from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False,  default='Free')
    price = models.IntegerField()
    duration = models.IntegerField()
    number_of_post = models.IntegerField()

    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, verbose_name='Profile Photo')
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('user', 'User')], default='user')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, default='Free')  # Corrected to Plan

    class Meta:
        db_table = 'custom_user'

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    product_picture = models.ImageField(upload_to='product_pictures/', null=True, blank=True, verbose_name='Product Picture')
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.IntegerField(blank=False, null=True)
    size = models.CharField(max_length=255, blank=False, null=False, default='')  # Assume this is what you meant by "area"
    location = models.CharField(max_length=255, blank=False, null=False, default='')
    descriptions = models.TextField(default='Anonymous')
    features = models.CharField(max_length=255, blank=False, null=False, default='')
    beds = models.CharField(max_length=20, blank=True, null=True, default='')  # Corrected max_length
    baths = models.CharField(max_length=10, blank=True, null=True, default='')  # Corrected max_length
    type = models.CharField(max_length=20, blank=True, null=True, default='')  # Corrected max_length

    class Meta:
        verbose_name_plural = 'Products'

class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    strip_id = models.CharField(max_length=255, blank=True, null=True, default='')

class Contact(models.Model):
    name = models.CharField(max_length=50, blank = True, null= True, default= 'Anonymous')
    subject = models.CharField(max_length=50, blank = True, null= True, default= 'Anonymous')
    email = models.EmailField()
    message = models.CharField(max_length=400, blank = True, null= True, default= 'Anonymous')
    date = models.DateTimeField(auto_now_add=True)