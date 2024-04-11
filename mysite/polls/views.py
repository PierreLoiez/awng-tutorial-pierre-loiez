from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils import timezone



# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list":latest_question_list
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

def results(request, question_id):
    response = "This is question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request, 
            "polls/detail.html", 
            {
                "question":question, 
                "error_message":"You didn't select a choice",
            },
        )
    
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
