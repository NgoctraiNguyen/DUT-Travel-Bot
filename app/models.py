from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Content(models.Model):
    name = models.CharField(max_length=128, null=True)
    last_tag = models.CharField(max_length=128, null=False)
    user = models.ForeignKey(User, models.CASCADE, null=True, default=None)


    def __str__(self) -> str:
        return str(self.name)
    

class Conservation(models.Model):
    user_question = models.CharField(max_length=128, null= True)
    bot_answer = models.CharField(max_length=128, null= True)
    conten = models.ForeignKey(Content, on_delete= models.SET_NULL, blank= True, null= True)
    


