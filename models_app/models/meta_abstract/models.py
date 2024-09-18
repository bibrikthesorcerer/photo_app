from django.db import models

class MetaAbstract(models.Model):
   class Meta:
      abstract = True
   
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)