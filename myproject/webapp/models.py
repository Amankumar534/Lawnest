from django.db import models

# Create your models here.

class Attorney(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/attorneys/')    
    position = models.TextField(max_length=100) 
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class News(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/news/')
    link = models.URLField(max_length=200, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title