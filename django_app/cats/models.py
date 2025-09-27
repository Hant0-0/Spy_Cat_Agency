from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=50)
    years_of_experience = models.IntegerField(default=0)
    breed = models.CharField(max_length=25)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


