import datetime
import django.contrib.auth.models

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question for model.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')
    current_vote = models.CharField(max_length=200)

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
        if now >= self.pub_date:
            return True
        return False

    def can_vote(self):
        """
        Check question which can be voted.
        """
        now = timezone.now()
        if self.is_published() and now <= self.end_date:
            return True
        return False


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


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)