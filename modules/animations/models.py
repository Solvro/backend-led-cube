from django.db import models


class Animation(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    animation = models.TextField()

    def __str__(self):
        return self.name
