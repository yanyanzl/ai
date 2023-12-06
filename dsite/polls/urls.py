# map views to URL

from django.urls import path

# import views.py from upper directory : polls
from . import views

app_name = "polls"

urlpatterns = [
    # The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.
    path("test", views.index1, ),
    path("", views.index, name="polls_index"),
    
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

]