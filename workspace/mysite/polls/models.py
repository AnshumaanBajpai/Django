from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone

## A class for the questions
@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    ## Adding a method to have a string representation of each Question object
    def __str__(self):
        return self.question_text
    
    ## A method to keep track of when the question was published
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    

## A class for options
@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    ## Adding a method to have a string representation of each Choice object
    def __str__(self):
        return self.choice_text