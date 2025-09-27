from django.db import models

from cats.models import Cat


class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE,
                            related_name="missions", blank=True, null=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


