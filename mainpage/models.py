from django.db import models

class Tables(models.Model):
    title = models.CharField("Оборудование", max_length=100)
    quantity=models.IntegerField("Количество")

    def __str__(self):
        return self.title

