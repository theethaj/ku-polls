from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("polls")


class IndexView(generic.ListView):
    """
    View for index.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())\
            .order_by('-pub_date')


class DetailView(generic.DetailView):
    """
    View for detail.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Return published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    View for results.
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    View for vote.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."})
    else:
        if question.can_vote():
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(
                reverse('polls:results', args=(question.id,))
            )
        else:
            messages.error(request, "Voting is not allowed.")
            return redirect('polls:index')


@receiver(user_logged_in)
def throw_login(sender, **kwargs):
    """
    Appears when logging in successfully.
    """
    log.info("You have successfully logged in.")


@receiver(user_logged_out)
def throw_logout(sender, **kwargs):
    """
    Appears when logging out successfully.
    """
    log.info("You have successfully logged out.")


@receiver(user_login_failed)
def throw_login_failed(sender, credentials, **kwargs):
    """
    Appears when logging in unsuccessfully.
    """
    log.warning("You have unsuccessfully logged in.")


def get_client_ip(request):
    """
    Get ip address from client.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip