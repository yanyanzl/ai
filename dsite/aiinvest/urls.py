# map views to URL

from django.urls import path

# import views.py from upper directory : aiinvest
from . import views

app_name = "aiinvest"

urlpatterns = [

    # Because Django’s URL resolver expects to send the request and associated arguments to a callable function, not a class, class-based views have an as_view() class method which returns a function that can be called when a request arrives for a URL matching the associated pattern. The function creates an instance of the class, calls setup() to initialize its attributes, and then calls its dispatch() method. dispatch looks at the request to determine whether it is a GET, POST, etc, and relays the request to a matching method if one is defined, or raises HttpResponseNotAllowed if not:
    # The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. 
    path("", views.index, name="index"),
    
    # in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".
    path("detail/<str:asset_name>/", views.detail, name="detail"),

     path("test/", views.test, name="test"),
    # The string may contain angle brackets (like <username> above) to capture part of the URL and send it as a keyword argument to the view. The angle brackets may include a converter specification (like the int part of <int:section>) which limits the characters matched and may also change the type of the variable passed to the view. For example, <int:section> matches a string of decimal digits and converts the value to an int.
    # str - Matches any non-empty string, excluding the path separator, '/'. This is the default if a converter isn’t included in the expression.
    # int - Matches zero or any positive integer. Returns an int.
    # slug - Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. For example, building-your-1st-django-site.
    # uuid - Matches a formatted UUID. To prevent multiple URLs from mapping to the same page, dashes must be included and letters must be lowercase. For example, 075194d3-6885-417e-a8a8-6c931e272f00. Returns a UUID instance.
    # path - Matches any non-empty string, including the path separator, '/'. This allows you to match against a complete URL path rather than a segment of a URL path as with str.
    path("result/", views.Result.result, name="result"),
 ]
'''
Eamples: 

    urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
]

Example requests:
/articles/2003 would not match any of these patterns, because each pattern requires that the URL end with a slash.

A request to /articles/2005/03/ would match the third entry in the list. Django would call the function views.month_archive(request, year=2005, month=3).

/articles/2003/03/building-a-django-site/ would match the final pattern. Django would call the function views.article_detail(request, year=2003, month=3, slug="building-a-django-site").
'''
   
