from django.db import models


class profile(models.Model):
    user=models.CharField(max_length=10,default='User')
    name=models.CharField(max_length=255)
    figma_file=models.URLField( max_length=200)
    
    def __str__(self):
        return self.user
