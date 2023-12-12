from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


# Here, each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.
class AssetData(models.Model):

    # The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.
    asset_name = models.CharField(max_length=200)
    asset_data_date = models.DateTimeField("date of the prices")
    asset_close_price = models.FloatField()
    asset_open_price = models.FloatField()
    asset_high_price = models.FloatField()
    asset_low_price = models.FloatField()
    asset_volume = models.BigIntegerField()

    # Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

    # define the return value for the object
    def __str__(self):
        return self.asset_name

# the list of assets could be selected
class AssetList(models.Model):

    asset_name = models.CharField(max_length=200)

    # define the return value for the object
    def __str__(self):
        return self.asset_name