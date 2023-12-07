
# define all the views for polls:

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# An F() object represents the value of a model field, transformed value of a model field, or annotated column. It makes it possible to refer to model field values and perform database operations using them without actually having to pull them out of the database into Python memory.

# Instead, Django uses the F() object to generate an SQL expression that describes the required operation at the database level.
from django.db.models import F

# import from polls/models.py
from .models import Question, Choice

# Each generic view needs to know what model it will be acting upon. This is provided using either the model attribute (in this example, model = Question for DetailView and ResultsView) or by defining the get_queryset() method (as shown in IndexView).
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    
    # For DetailView the question variable is provided automatically – since we’re using a Django model (Question), Django is able to determine an appropriate name for the context variable. However, for ListView, the automatically generated context variable is question_list. To override this we provide the context_object_name attribute, specifying that we want to use latest_question_list instead.
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

# By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html. In our case, it would use the template "polls/question_detail.html". The template_name attribute is used to tell Django to use a specific template name instead of the autogenerated default template name. 
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# We also specify the template_name for the results list view – this ensures that the results view and the detail view have a different appearance when rendered, even though they’re both a DetailView behind the scenes
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def index1(request):
    return HttpResponse("Hello, world. this is the first page i created!")

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # That code loads the template called polls/index.html 
    template = loader.get_template("polls/index.html")

    # create a dictionary as a context. 
    # this will be passed to render as an input args to render template.

    context = {
        "latest_question_list": latest_question_list,
    }
    # passes the template a context. The context is a dictionary mapping template variable names to Python objects.
    return HttpResponse(template.render(context,request))

    # or by 
    # return render(request, "polls/index.html", context)
    # The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.


# When somebody requests a page from your website – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the patterns in order. After finding the match at 'polls/', it strips off the matching text ("polls/") and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing. There it matches '<int:question_id>/', resulting in a call to the detail() view like so:

# detail(request=<HttpRequest object>, question_id=34)

# The question_id=34 part comes from <int:question_id>. Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function. The question_id part of the string defines the name that will be used to identify the matched pattern, and the int part is a converter that determines what patterns should match this part of the URL path. The colon (:) separates the converter and pattern name.

# loose coupling
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

'''
# controlled coupling is introduced in the django.shortcuts module use this way

from django.shortcuts import get_object_or_404, render
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
'''


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    # question_id come from the url. which generated by the form in detail.html
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The bellow code checks for KeyError and redisplays the question form with an error message if choice isn’t given.
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                # context for render the page. two inputs now. one for question
                "question": question,
                # one for error_message
                "error_message": "You didn't select a choice. Please select one",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
        # the reverse() function in the HttpResponseRedirect constructor. This function helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view. using the URLconf, this reverse() call will return a string "/polls/3/results/"
        # where the 3 is the value of question.id. This redirected URL will then call the 'results' view to display the final page.
        # After somebody votes in a question, the vote() view redirects to the results page for the question