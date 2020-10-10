import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question for model.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def __str__(self):
        """
        String.
        """
        return self.question_text

    def was_published_recently(self):
        """
        Check recently published question.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """
        Check published question.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        Check question which can be voted.
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """
    Choice for model.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Return choice text.
        """
        return self.choice_text
