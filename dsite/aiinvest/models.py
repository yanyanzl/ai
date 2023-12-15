from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone




# the list of assets could be selected
class AssetList(models.Model):

    asset_name = models.CharField(max_length=200)

    # define the return value for the object
    def __str__(self):
        return self.asset_name
    

# Here, each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.
class AssetData(models.Model):

    # The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.
    asset_name = models.CharField(max_length=200)
    date = models.DateTimeField("date for the prices")
    close = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.BigIntegerField()
    asset = models.ForeignKey(AssetList, on_delete=models.CASCADE)

    # Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

    # define the return value for the object
    def __str__(self):
        return self.asset_name