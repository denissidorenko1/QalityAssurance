from django.db import models

class Tables(models.Model):
    title = models.CharField("Оборудование", max_length=100)
    quantity=models.IntegerField("Количество")
    def __str__(self):
        return self.title


class Contributors(models.Model):
    title=models.CharField("ФИО", max_length=120)
    bio=models.TextField("БИО")
    contributor_id = models.IntegerField("id")
    def __str__(self):
        return self.title