from django.db import models


class Token(models.Model):
    status = models.BooleanField(default=True)
