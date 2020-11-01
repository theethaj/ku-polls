import datetime

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


class QuestionIndexViewTests(TestCase):
    """
    Test question index view.
    """
    def test_no_questions(self):
        """
        Test zero avaliable questions. If yes, return a message.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Test question by past. If yes, return a question in the past.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Test question by future.
        If yes, a question in the future will not be returned.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Test one question by past and another one by future.
        If yes, return a question in the past.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        Test two questions by past. If yes, return both.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>',
             '<Question: Past question 1.>']
        )
