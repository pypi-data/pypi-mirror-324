from _typeshed import Incomplete
from django.db import models

class BaseEntityAbstractModel(models.Model):
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        abstract: bool
