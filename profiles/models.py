from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    hobbies = models.CharField(max_length=1000)
    
    def __unicode__(self):
      return self.name

class PublicProfile(models.Model):
    profile = models.OneToOneField(Profile)
    
    public_bio = models.CharField(max_length=1000, blank=True, null=True)