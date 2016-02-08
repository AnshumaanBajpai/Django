from django.http import HttpResponseRedirect
# RequestContext and loader not needed if we use render
# from django.template import RequestContext, loader

from django.shortcuts import render, get_object_or_404
from polls.models import Question, Choice

from django.core.urlresolvers import reverse


# Creating the views for polls application

# creating a view for the index of questions
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template("polls/index.html")
    #context = RequestContext(request, {
    #                                   'latest_question_list': latest_question_list,
    #                                   })
    #return HttpResponse(template.render(context))
    # An alternate short approach to returning the rendering
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# Creating a view for the details of the question
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

# Creating a view for the results #most recent
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

# Creating a view for the vote
def vote(request, question_id): #most recent
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
                                                     'question':p,
                                                     'error_message': "You didn't select a choice",
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    
