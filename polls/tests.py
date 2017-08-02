import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question


# Create your tests here.
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day
        :return:
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


def create_quetion(question_text, days):
    """
    Create a question with the given 'question_text' published the given
    number of 'days' offset to now (negative for question published
    in the past, positive for question that have yet to be published).
    :param question_text: text for question
    :param days: negative => in the past, positive => in the future
    :return: Question object
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):

    def test_index_view_with_no_question(self):
        """
        If no question exist, an appropriate message should be displayed
        on the index page.
        :return:
        """
        responce = self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, 'No polls are available.')
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed
        on the index page.
        :return:
        """
        create_quetion(question_text='Past question.', days=-30)
        responce = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            responce.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Question with a pub_date in the future should not be displayed
        on the index page.
        :return:
        """
        create_quetion(question_text='Future question.', days=30)
        responce = self.client.get(reverse('polls:index'))
        self.assertContains(responce, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_questions(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        :return:
        """
        create_quetion(question_text='Past question.', days=-30)
        create_quetion(question_text='Future question.', days=30)
        responce = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            responce.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_question(self):
        """
        The question index page may display multiple questions.
        :return:
        """
        create_quetion(question_text='Past question 1.', days=-30)
        create_quetion(question_text='Past question 2.', days=-5)
        responce = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            responce.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionIndexDetailTests(TestCase):

    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        should return a 404 not found.
        :return:
        """
        future_question = create_quetion(question_text='Future question.', days=5)
        responce = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(responce.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The datail view of a question with a pub_date in the past
        should display the question's text.
        :return:
        """
        past_question = create_quetion(question_text='Past question.', days=-5)
        responce = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(responce, past_question.question_text, status_code=200)
