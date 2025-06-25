from django.db import models

class Actor_Detail(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"Actor name is {self.name}"
