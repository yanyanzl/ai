
# define all the views for polls:

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http import Http404

# import from polls/models.py
from .models import Question

def index1(request):
    return HttpResponse("Hello, world. this is the first page i created!")

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # That code loads the template called polls/index.html 
    template = loader.get_template("polls/index.html")

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
    response = "You're looking at the results of question  %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)