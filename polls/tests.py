import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


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
        Test recently published question by future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Test recently published question by past.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Test recently published question by now.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        Test published question by future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_old_question(self):
        """
        Test published question by past.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_is_published_with_recent_question(self):
        """
        Test published question by now.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.is_published())

    def test_can_vote_with_future_question(self):
        """
        Test question which can be voted by future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_old_question(self):
        """
        Test question which can be voted by past.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertFalse(old_question.can_vote())

    def test_can_vote_with_recent_question(self):
        """
        Test question which can be voted by now.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        recent_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertTrue(recent_question.can_vote())


class QuestionIndexViewTests(TestCase):
    """
    Test question index view.
    """
    def test_no_questions(self):
        """
        Test zero avaliable questions.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Test question by past.
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
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Test one question by past and another one by future.
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
        Test two questions by past.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>',
             '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """
    Test question detail view.
    """
    def test_future_question(self):
        """
        Test question detail view by future.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Test question detail view by past.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
