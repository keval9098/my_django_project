from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Questions, Choice, Voters
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""

        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Questions
    context_object_name = 'question'
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Questions
    context_object_name = 'question'
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    #current_user = request.user
    #q=Voters(user_number=request.user.id)
    #q.save()
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #if  Voters.objects.filter(user_number=request.user.id).exists():
        #     return render(request, 'polls/detail.html', {
           # 'question': question,
          #  'error_message': "You have already voted.",
       # })
        #else:
        selected_choice.vote += 1
        selected_choice.save()
            
            

        

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
