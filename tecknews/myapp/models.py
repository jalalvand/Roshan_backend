from django.db import models

class NewPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.CharField(max_length=200)
    resource = models.TextField()
    def __str__(self):
    	return self.title