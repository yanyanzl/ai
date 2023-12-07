# define your models – essentially, your database layout, with additional metadata.


# That small bit of model code gives Django a lot of information. With it, Django is able to:
# Create a database schema (CREATE TABLE statements) for this app.
# Create a Python database-access API for accessing Question and Choice objects.


import datetime
from django.db import models
from django.utils import timezone


# Here, each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.
class Question(models.Model):

    # The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

    # define the return value for the object
    def __str__(self):
        return self.question_text
    
    # published recently or not
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    # note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # define the return value for the object
    def __str__(self):
        return self.choice_text

