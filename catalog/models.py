from django.db import models

# Create your models here.
class Lead(models.Model):

    name = models.CharField(max_length=200, help_text="Enter lead name")
    email = models.CharField(max_length=200, help_text="Enter lead email")
    status = models.CharField(max_length=200, help_text="Enter lead email")

    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of Lead.
         """
         return reverse('lead-detail-view', args=[str(self.id)])
    
    def __str__(self):
        
        return self.email
