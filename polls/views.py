from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Question


# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context_dict = {
        'latest_question_list': latest_question_list,
    }
    # context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context_dict))


def detail(request, question_id):
    return HttpResponse('You\'re looking at question {}.'.format(question_id))


def results(request, question_id):
    response = 'You\'re looking at the results of question {}.'
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse('You\'re voting on question {}.'.format(question_id))
