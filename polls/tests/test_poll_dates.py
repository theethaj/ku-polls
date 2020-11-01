import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days, duration=1):
    """
    Create a question with the given question_text, given number of days offset to now.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end = time + datetime.timedelta(days=duration)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time, end_date=end)


class QuestionModelTests(TestCase):
    """
    Test question model.
    """
    def test_was_published_recently_with_future_question(self):
        """
        Test recently published question by future. If yes, return False.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Test recently published question by past. If yes, return False.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Test recently published question by now. If yes, return True.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        Test published question by future. If yes, return False.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_old_question(self):
        """
        Test published question by past. If yes, return True.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_is_published_with_recent_question(self):
        """
        Test published question by now. If yes, return True.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.is_published())

    def test_can_vote_with_future_question(self):
        """
        Test question which can be voted by future. If yes, return False.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_old_question(self):
        """
        Test question which can be voted by past. If yes, return False.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertFalse(old_question.can_vote())

    def test_can_vote_with_recent_question(self):
        """
        Test question which can be voted by now. If yes, return True.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        recent_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertTrue(recent_question.can_vote())
