from django.db import models

class AgentsModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)

class LatituteAndLongituteModel(models.Model):
    id = models.AutoField(primary_key=True)
    agents = models.ForeignKey(AgentsModel,on_delete=models.CASCADE)
    latitute = models.FloatField()
    longitute = models.FloatField()

class GivenPlaces(models.Model):
    id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    latitute = models.FloatField()
    longitute = models.FloatField()

