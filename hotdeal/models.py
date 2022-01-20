from django.db import models

# Create your models here.
class Deal(models.Model):
    image_url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200, primary_key=True)
    reply_count = models.IntegerField()
    up_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-created_at']
    
