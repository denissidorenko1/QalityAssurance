from django.db import models

class Tables(models.Model):
    equip = models.CharField("Оборудование", max_length=100)
    quantity=models.IntegerField("Количество")
    approved_by_manager=models.BooleanField(default=0)
    delivered=models.BooleanField(default=0)
    def __str__(self):
        return self.equip


class Contributors(models.Model):
    title=models.CharField("ФИО", max_length=120)
    bio=models.TextField("БИО")
    contributor_id = models.IntegerField("id")

    def __str__(self):
        return self.title


