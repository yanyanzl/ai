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

# Database setup

    # Now, open up mysite/settings.py. It’s a normal Python module with module-level variables representing Django settings.
    # By default, the configuration uses SQLite. If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database.

    # If you wish to use another database, install the appropriate database bindingslike bellow
        # If you’re using PostgreSQL, you’ll need the psycopg or psycopg2 package: pip install psycopg2 or conda install psycopg2
        # change the following keys in the DATABASES 'default' item to match your database connection settings:
            # DATABASES = {
            #     "default": {
            #         "ENGINE": "django.db.backends.postgresql_psycopg2",
            #         "NAME": "[YOUR_DATABASE_NAME]",
            #         "USER": "[YOUR_USER_NAME]",
            #         "PASSWORD": "",
            #         "HOST": "localhost",
            #         "PORT": "",
            #     }
            # }

    # Some of these applications make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command:
        # python manage.py migrate
        # The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py file and the database migrations shipped with the app (we’ll cover those later). You’ll see a message for each migration it applies. If you’re interested, run the command-line client for your database and type \dt (PostgreSQL)

# Creating models
    # define your models in models.py, the database layout with additional metadata.
    # Don’t repeat yourself (DRY) principle: Every distinct concept and/or piece of data should live in one, and only one, place. Redundancy is bad. Normalization is good.

    # Activating models: we need to tell our project that the polls app is installed. Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation. 
    # To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file, so its dotted path is 'polls.apps.PollsConfig'. Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this:
        # mysite/settings.py
        # INSTALLED_APPS = [
        #     "polls.apps.PollsConfig",
        #     "django.contrib.admin",
        #     ...
        # ]
        # Now Django knows to include the polls app

    # Prepare for migration.  :
        # python manage.py makemigrations polls
        
        # By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.
        
        # Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. You can read the migration for your new model if you like; it’s the file polls/migrations/0001_initial.py. 

        # There’s a command that will run the migrations for you and manage your database schema automatically. The sqlmigrate command takes migration names and returns their SQL. The sqlmigrate command doesn’t actually run the migration on your database - instead, it prints it to the screen so that you can see what SQL Django thinks is required. It’s useful for checking what Django is going to do or if you have database administrators who require SQL scripts for changes.
        # python manage.py sqlmigrate polls 0001

        # python manage.py check 
            # this checks for any problems in your project without making migrations or touching the database.

    # Migrate: run migrate to create those model tables in your database:
        # python manage.py migrate
        # The migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using a special table in your database called django_migrations) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

# Playing with the API
    # python manage.py shell
    # We’re using this instead of simply typing “python”, because manage.py sets the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file.
        
'''
        >>> from polls.models import Choice, Question  # Import the model classes we just wrote.

        # No questions are in the system yet.
        >>> Question.objects.all()
        <QuerySet []>

        # Create a new Question.
        # Support for time zones is enabled in the default settings file, so
        # Django expects a datetime with tzinfo for pub_date. Use timezone.now()
        # instead of datetime.datetime.now() and it will do the right thing.
        >>> from django.utils import timezone
        >>> q = Question(question_text="What's new?", pub_date=timezone.now())

        # Save the object into the database. You have to call save() explicitly.
        >>> q.save()

        # Now it has an ID.
        >>> q.id
        1

        # Access model field values via Python attributes.
        >>> q.question_text
        "What's new?"
        >>> q.pub_date
        datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

        # Change values by changing the attributes, then calling save().
        >>> q.question_text = "What's up?"
        >>> q.save()

        # objects.all() displays all the questions in the database.
        >>> Question.objects.all()
        <QuerySet [<Question: Question object (1)>]>
        '''

'''
        >>> from polls.models import Choice, Question

        # Make sure our __str__() addition worked.
        >>> Question.objects.all()
        <QuerySet [<Question: What's up?>]>

        # Django provides a rich database lookup API that's entirely driven by
        # keyword arguments.
        >>> Question.objects.filter(id=1)
        <QuerySet [<Question: What's up?>]>
        >>> Question.objects.filter(question_text__startswith="What")
        <QuerySet [<Question: What's up?>]>

        # Get the question that was published this year.
        >>> from django.utils import timezone
        >>> current_year = timezone.now().year
        >>> Question.objects.get(pub_date__year=current_year)
        <Question: What's up?>

        # Request an ID that doesn't exist, this will raise an exception.
        >>> Question.objects.get(id=2)
        Traceback (most recent call last):
            ...
        DoesNotExist: Question matching query does not exist.

        # Lookup by a primary key is the most common case, so Django provides a
        # shortcut for primary-key exact lookups.
        # The following is identical to Question.objects.get(id=1).
        >>> Question.objects.get(pk=1)
        <Question: What's up?>

        # Make sure our custom method worked.
        >>> q = Question.objects.get(pk=1)
        >>> q.was_published_recently()
        True

        # Give the Question a couple of Choices. The create call constructs a new
        # Choice object, does the INSERT statement, adds the choice to the set
        # of available choices and returns the new Choice object. Django creates
        # a set to hold the "other side" of a ForeignKey relation
        # (e.g. a question's choice) which can be accessed via the API.
        >>> q = Question.objects.get(pk=1)

        # Display any choices from the related object set -- none so far.
        >>> q.choice_set.all()
        <QuerySet []>

        # Create three choices.
        >>> q.choice_set.create(choice_text="Not much", votes=0)
        <Choice: Not much>
        >>> q.choice_set.create(choice_text="The sky", votes=0)
        <Choice: The sky>
        >>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

        # Choice objects have API access to their related Question objects.
        >>> c.question
        <Question: What's up?>

        # And vice versa: Question objects get access to Choice objects.
        >>> q.choice_set.all()
        <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
        >>> q.choice_set.count()
        3

        # The API automatically follows relationships as far as you need.
        # Use double underscores to separate relationships.
        # This works as many levels deep as you want; there's no limit.
        # Find all Choices for any question whose pub_date is in this year
        # (reusing the 'current_year' variable we created above).
        >>> Choice.objects.filter(question__pub_date__year=current_year)
        <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

        # Let's delete one of the choices. Use delete() for that.
        >>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
        >>> c.delete()

        For more information on model relations, see Accessing related objects. For more on how to use double underscores to perform field lookups via the API, see Field lookups. For full details on the database API, see our Database API reference.
        '''

# Introducing the Django Admin
    # Generating admin sites for your staff or clients to add, change, and delete content is tedious work that doesn’t require much creativity. For that reason, Django entirely automates creation of admin interfaces for models.

    # Django was written in a newsroom environment, with a very clear separation between “content publishers” and the “public” site. Site managers use the system to add news stories, events, sports scores, etc., and that content is displayed on the public site. Django solves the problem of creating a unified interface for site administrators to edit content.

    # The admin isn’t intended to be used by site visitors. It’s for site managers.

    # Creating an admin user: python manage.py createsuperuser
    # now you can login to the site http://127.0.0.1:8000/admin/ by admin

    # Make the poll app modifiable in the admin. we need to tell the admin that Question objects have an admin interface. To do this, open the polls/admin.py file, and edit it to look like this:
        # from django.contrib import admin

        # from .models import Question

        # admin.site.register(Question)

# Views : web pages
    # In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views)

    # To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views. refer to URL dispatcher for more information.

    # Write views that actually do something
    # Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

    # Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, using whatever Python libraries you want.

    # All Django wants is that HttpResponse. Or an exception.

# Template for Views:
    # create a directory called templates in your polls directory. Django will look for templates in there.

    # Your project’s TEMPLATES setting describes how Django will load and render templates. The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True. By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS.

    # Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html. In other words, your template should be at polls/templates/polls/index.html. Because of how the app_directories template loader works as described above, you can refer to this template within Django as polls/index.html.

    # Use the template system
'''
        <h1>{{ question.question_text }}</h1>
        <ul>
        {% for choice in question.choice_set.all %}
            <li>{{ choice.choice_text }}</li>
        {% endfor %}
        </ul>
'''
    # The template system uses dot-lookup syntax to access variable attributes. In the example of {{ question.question_text }}, first Django does a dictionary lookup on the object question. Failing that, it tries an attribute lookup – which works, in this case. If attribute lookup had failed, it would’ve tried a list-index lookup.
    # Method-calling happens in the {% for %} loop: question.choice_set.all is interpreted as the Python code question.choice_set.all(), which returns an iterable of Choice objects and is suitable for use in the {% for %} tag.

    # See the template guide for more about templates

    # Removing hardcoded URLs in templates
    # from :
    # <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    # to :
    # <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
    
    # The way this works is by looking up the URL definition as specified in the polls.urls module. You can see exactly where the URL name of ‘detail’ is defined below:
    # the 'name' value as called by the {% url %} template tag
    # path("<int:question_id>/", views.detail, name="detail"),


# Namespaceing URL names 

    # For example, the polls app has a detail view, and so might an app on the same project that is for a blog. How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

    # The answer is to add namespaces to your URLconf. In the polls/urls.py file, go ahead and add an app_name to set the application namespace: app_name = "polls"
    
    # Now change your polls/index.html to like: 
        # <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>

# Use generic views: Less code is better
    # Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app. For example, the ListView and DetailView generic views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object” respectively.

        # Generic display views: The two following generic class-based views are designed to display data
            # django.views.generic.detail.DetailView : While this view is executing, self.object will contain the object that the view is operating upon.
            # django.views.generic.list.ListView : A page representing a list of objects.
                # While this view is executing, self.object_list will contain the list of objects (usually, but not necessarily a queryset) that the view is operating upon.

        # Generic editing views
            # The following views provide a foundation for editing content:
            # django.views.generic.edit.FormView : A view that displays a form. On error, redisplays the form with validation errors; on success, redirects to a new URL.
            # django.views.generic.edit.CreateView : A view that displays a form for creating an object, redisplaying the form with validation errors (if there are any) and saving the object.
            # django.views.generic.edit.UpdateView
            # django.views.generic.edit.DeleteView


        # Generic date views:
            # django.views.generic.dates,  views from it for displaying drilldown pages for date-based data.
            
            # django.views.generic.dates.ArchiveIndexView : A top-level index page showing the “latest” objects, by date. Objects with a date in the future are not included unless you set allow_future to True.
            
            # django.views.generic.dates.YearArchiveView : A yearly archive page showing all available months in a given year. Objects with a date in the future are not displayed unless you set allow_future to True.
            
            # django.views.generic.dates.MonthArchiveView : A monthly archive page showing all objects in a given month. Objects with a date in the future are not displayed unless you set allow_future to True.

            # django.views.generic.dates.WeekArchiveView : A weekly archive page showing all objects in a given week. Objects with a date in the future are not displayed unless you set allow_future to True.

            # django.views.generic.dates.DayArchiveView : A day archive page showing all objects in a given day. Days in the future throw a 404 error, regardless of whether any objects exist for future days, unless you set allow_future to True.

            # django.views.generic.dates.TodayArchiveView : A day archive page showing all objects for today. This is exactly the same as django.views.generic.dates.DayArchiveView, except today’s date is used instead of the year/month/day arguments.

            # django.views.generic.dates.DateDetailView : A page representing an individual object. If the object has a date value in the future, the view will throw a 404 error by default, unless you set allow_future to True.

# A conventional place for an application’s tests is in the application’s tests.py file; the testing system will automatically find tests in any file whose name begins with test.
    
    # after build test cased in test.py. execute command : python manage.py test polls

    # The Django test client in the shell: 
        # python manage.py shell
        # from django.test.utils import setup_test_environment
        # setup_test_environment()
        # from django.test import Client
        # client = Client()  # create an instance of the client for our use
        # from django.urls import reverse 
        # response = client.get(reverse("polls:index"))
        # response.status_code
        # response.content
        # response.context["latest_question_list"]


# Customize your app’s look and feel
    # Aside from the HTML generated by the server, web applications generally need to serve additional files — such as images, JavaScript, or CSS — necessary to render the complete web page. In Django, we refer to these files as “static files”.

    # Make sure that django.contrib.staticfiles is included in your INSTALLED_APPS.
    # In your settings file, define STATIC_URL, for example: STATIC_URL = "static/"
    # The default will find files stored in the STATICFILES_DIRS setting (using django.contrib.staticfiles.finders.FileSystemFinder) and in a static subdirectory of each app (using django.contrib.staticfiles.finders.AppDirectoriesFinder). If multiple files with the same name are present, the first file that is found will be used.
    

    # First, create a directory called static in your polls directory. Django will look for static files there


# python -c "import django; print(django.__path__)"
# the above command finding where the Django source files are located on your system

# Plug-in third-party packages
    # Django Debug Toolbar : python -m pip install django-debug-toolbar
    # he toolbar helps you understand how your application functions and to identify problems. It does so by providing panels that provide debug information about the current request and response.

    # Third-party packages that integrate with Django need some post-installation setup to integrate them with your project. Often you will need to add the package’s Django app to your INSTALLED_APPS setting. Some packages need other changes, like additions to your URLconf (urls.py).

import django

print(django.get_version())

