from django.db import models


class ModelMixIn(models.Model):

    class Meta:
        abstract = True

    def get_all(cls):
        return cls.objects.all()
