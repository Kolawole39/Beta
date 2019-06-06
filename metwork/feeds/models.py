from django.db import models

# Create your models here.

class Event(models.Model):
    Eventer = models.CharField(max_length = 100)
    title = models.CharField(max_length=50)
    description = models.TextField() 
    upload = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        "Renvoie une representation du post"
        return "Crée par {} le {} \n. {}".format(self.Eventer, str(self.date_added), self.description[:50])

class Comment(models.Model):
    commentor = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey('Event',on_delete=models.CASCADE)   
    text = models.TextField()
    
    def __str__(self):
        "Renvoie une representation du commentaire"
        return "Crée par {} le {}. \n {}".format(self.commentor, str(self.date_added), self.text[:50])
