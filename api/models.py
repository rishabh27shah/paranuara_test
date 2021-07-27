from django.db import models


class Company(models.Model):
    """
    Company: properties- company_name
    """
    company_name = models.CharField(max_length=255)


class People(models.Model):
    """
    People: properties- name, age, address, phone,
    has_died, eye_color, fruits, vegetables, friends, company
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=100)
    has_died = models.BooleanField()
    eye_color = models.CharField(max_length=50)
    fruits = models.TextField(null=True)
    vegetables = models.TextField(null=True)
    friends = models.ManyToManyField("self", symmetrical=False)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True
    )
