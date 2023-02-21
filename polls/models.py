from django.db import models
from django.contrib import admin

from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Is Published recently?',
    )
    def was_published_recently(self):
        # print(timedelta(days=1))
        return timezone.now() >= self.pub_date >= timezone.now() - timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# >>> q.was_published_recently()
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
#   File "C:\playground\fullstack\django-pr\demo\mysite\polls\models.py", line 17, in was_published_recently
#     print(datetime.timedelta(days=1))
# AttributeError: module 'datetime' has no attribute 'delta'
