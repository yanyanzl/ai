# map views to URL

from django.urls import path

# import views.py from upper directory : polls
from . import views

urlpatterns = [
    # The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.
    path("test", views.index1, name="index"),
]