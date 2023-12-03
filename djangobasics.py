# to learn basics about django
# Django makes it easier to build better web apps more quickly and with less code.

# Django (/ˈdʒæŋɡoʊ/ JANG-goh; sometimes stylized as django)[6] is a free and open-source, Python-based web framework that follows the model–template–views (MTV) architectural pattern.[7][8] It is maintained by the Django Software Foundation (DSF), an independent organization established in the US as a 501(c)(3) non-profit.

# Django's primary goal is to ease the creation of complex, database-driven websites. The framework emphasizes reusability and "pluggability" of components, less code, low coupling, rapid development, and the principle of don't repeat yourself.[9] Python is used throughout, even for settings, files, and data models. Django also provides an optional administrative create, read, update and delete interface that is generated dynamically through introspection and configured via admin models.

# Step 1 
# create a mysite directory in your current directory by command: 
# django-admin startproject mysite
# look at what startproject created:
# mysite/
#     manage.py
#     mysite/
#         __init__.py
#         settings.py
#         urls.py
#         asgi.py
#         wsgi.py

# These files are:

# The outer mysite/ root directory is a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
# manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py.
# The inner mysite/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
# mysite/__init__.py: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.
# mysite/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.
# mysite/urls.py: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.
# mysite/asgi.py: An entry-point for ASGI-compatible web servers to serve your project. See How to deploy with ASGI for more details.
# mysite/wsgi.py: An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.

# step 2 run the server for your website, back to outer mysit/
# python manage.py runserver

# or specify ip or port number by
# python manage.py runserver 0.0.0.0:8000
# don’t use this server in anything resembling a production environment. It’s intended only for use while developing.
# the development enviorenment is ready now

# step 3 creating apps
# To create your app, make sure you’re in the same directory as manage.py and type this command:
# python manage.py startapp polls
# That’ll create a directory polls, which is laid out like this:
# polls/
#     __init__.py
#     admin.py
#     apps.py
#     migrations/
#         __init__.py
#     models.py
#     tests.py
#     views.py

# step 4 write views
# Write your first view: Open the file polls/views.py and edite it

# step 5 map the view to a URL
# To call the view, we need to map it to a URL - and for this we need a URLconf.
# To create a URLconf in the polls directory, create a file called urls.py
# add these codes:
# from django.urls import path

# from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
# ]

# step 6 set URLconf in root directory
# point the root URLconf at the polls.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

# from django.contrib import admin
# from django.urls import include, path

# urlpatterns = [
#     path("polls/", include("polls.urls")),
#     path("admin/", admin.site.urls),
# ]

# The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

# The idea behind include() is to make it easy to plug-and-play URLs. Since polls are in their own URLconf (polls/urls.py), they can be placed under “/polls/”, or under “/fun_polls/”, or under “/content/polls/”, or any other path root, and the app will still work.

# How Django processes a request¶
# When a user requests a page from your Django-powered site, this is the algorithm the system follows to determine which Python code to execute:

# Django determines the root URLconf module to use. Ordinarily, this is the value of the ROOT_URLCONF setting, but if the incoming HttpRequest object has a urlconf attribute (set by middleware), its value will be used in place of the ROOT_URLCONF setting.

# Django loads that Python module and looks for the variable urlpatterns. This should be a sequence of django.urls.path() and/or django.urls.re_path() instances.

# Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL, matching against path_info.    
# Once one of the URL patterns matches, Django imports and calls the given view, which is a Python function (or a class-based view). The view gets passed the following arguments:
    # An instance of HttpRequest.
    # If the matched URL pattern contained no named groups, then the matches from the regular expression are provided as positional arguments.
    # The keyword arguments are made up of any named parts matched by the path expression that are provided, overridden by any arguments specified in the optional kwargs argument to django.urls.path() or django.urls.re_path().
# If no URL pattern matches, or if an exception is raised during any point in this process, Django invokes an appropriate error-handling view. See Error handling below.

import django

print(django.get_version())
