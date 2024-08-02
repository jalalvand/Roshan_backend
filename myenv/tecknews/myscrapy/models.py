from django.db import models

# # Create your models here.
# class Article(models.Model):
#     title = models.CharField(max_length=300)
    
#     link = models.URLField()
#     def __str__(self):
#         return self.title
    
class Article(models.Model):
    url = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.CharField(max_length=200)
    resource = models.TextField()
    def __str__(self):
    	return self.title