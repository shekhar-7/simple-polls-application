from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

# Create your views here.


def index(req):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    data = ', '.join(q.question_text for q in latest_question_list)
    # return HttpResponse("Hello world! polls app\n %s" % data)
    return render(req, 'polls/index.html', context={'latest_question_list': latest_question_list})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def detail(req, question_id):
    # try:
    #     q = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question Does not exist")
    q = get_object_or_404(Question, pk=question_id)
    return render(req, 'polls/detail.html', context={'question': q})


def results(req, question_id):
    data = "You are on results page %s" % question_id
    question = get_object_or_404(Question, pk=question_id)

    return render(req, 'polls/results.html', {'question': question})


def vote(req, question_id):
    data = "You are on vote page %s" % question_id
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(req)
        selected_choice = question.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(req, 'polls/detail.html', {
            'question': question,
            'error_message': "please select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
