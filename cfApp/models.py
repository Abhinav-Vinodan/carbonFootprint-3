from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Experts(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    aadhar = models.CharField(max_length=12)
    qual = models.CharField(max_length=12)
    proof = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tips(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    subject = models.CharField(max_length=50)
    details = models.CharField(max_length=300)
    image = models.FileField(null=True)
    experts = models.ForeignKey(Experts, on_delete=models.CASCADE)



class Category(models.Model):
    cat = models.CharField(max_length=50)
    status = models.CharField(max_length=20,default='Active')


class Emission(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    device_power = models.CharField(max_length=30)
    hours_per_day = models.CharField(max_length=30)
    lifespan_years = models.CharField(max_length=30)
    no_of_devices = models.CharField(max_length=30)
    electricity_emission_factor = models.CharField(max_length=30,default=0.5)
    result = models.CharField(max_length=30,null=True)
    charge = models.CharField(max_length=30,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)


class Message(models.Model):
    experts=models.ForeignKey(Experts,on_delete=models.CASCADE)
    users=models.ForeignKey(Users,on_delete=models.CASCADE)
    sender=models.CharField(max_length=50)
    msg=models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    feedback=models.CharField(max_length=500)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)