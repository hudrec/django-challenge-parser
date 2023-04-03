from django.db import models


# Create your models here.
class Page(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    pages = models.ManyToManyField("core.Page", blank=True, related_name='details')

    def __str__(self):
        return self.name