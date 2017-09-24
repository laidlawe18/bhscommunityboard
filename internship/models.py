from __future__ import unicode_literals

from django.db import models

# Create your models here.
class InternshipOpportunity(models.Model):
    
    name = models.CharField(max_length=40)
    description = models.TextField()
    number_of_openings = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name