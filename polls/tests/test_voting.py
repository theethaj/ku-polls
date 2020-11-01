import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days, duration=1):
    """
    Create a question with the given question_text, given number of days offset to now.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end = time + datetime.timedelta(days=duration)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time, end_date=end)


class VotingTests(TestCase):
    """
    Test voting.
    """
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user("Daniel", "daniel.j@ku.th", "abc007")
        user.first_name = 'Daniel'
        user.last_name = "James"
        user.save()

    def test_vote_with_authentication(self):
        self.client.login(username="Daniel", password="abc007")
        question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:vote', args=question.id))
        self.assertEqual(response.status_code, 200)

    def test_vote_with_no_authentication(self):
        question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:vote', args=question.id))
        self.assertEqual(response.status_code, 302)