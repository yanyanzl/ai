# map views to URL

from django.urls import path

# import views.py from upper directory : polls
from . import views

app_name = "polls"

urlpatterns = [

    # Because Django’s URL resolver expects to send the request and associated arguments to a callable function, not a class, class-based views have an as_view() class method which returns a function that can be called when a request arrives for a URL matching the associated pattern. The function creates an instance of the class, calls setup() to initialize its attributes, and then calls its dispatch() method. dispatch looks at the request to determine whether it is a GET, POST, etc, and relays the request to a matching method if one is defined, or raises HttpResponseNotAllowed if not:
    # The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. 
    path("", views.IndexView.as_view(), name="index"),
    
    # in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
    
    ]
''' this is hard code. the other one use generic views in django
    path("test", views.index1, ),
    path("", views.index, name="polls_index"),
    
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
'''