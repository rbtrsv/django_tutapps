from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# Create your views here.

# View (function-based)
# The index function below is exactly like index in catalog.views 
# def index(request): 
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     # We call render() to pass the list to a specified template
#     return render(request, 'polls/index.html', context) 

# View (class-based)
# Use a class-based generic list view (ListView) — a class that inherits from an existing view.
# Because the generic view already implements most of the functionality we need and follows Django best-practice, we will be able to create a more robust list view with less code.
class IndexView(generic.ListView):
    template_name = 'polls/polls_index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            # __lte returns all objects whose pub_date is either less than or equal to the current time zone.
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]



# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls_app/results.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data by key name.
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string.

        # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The below code checks for KeyError and redisplays the question form with an error message if choice isn’t given.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        # After incrementing the choice count, the code returns an HttpResponseRedirect rather than a normal HttpResponse. 
        # HttpResponseRedirect takes a single argument: the URL to which the user will be redirected.

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # We are using the reverse() function in the HttpResponseRedirect constructor in this example. 
        # This function helps avoid having to hardcode a URL in the view function.
        # In this case, using the URLconf we set up in polls/urls.py, this reverse() call will return a string like '/polls/3/results/' where the 3 is the value of question.id.
        # This redirected URL will then call the 'results' view to display the final page.