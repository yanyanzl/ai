"""dsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# this is the list for all the mappings in root directory

# When somebody requests a page from your website – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the patterns in order. After finding the match at 'polls/', it strips off the matching text ("polls/") and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing. There it matches '<int:question_id>/', resulting in a call to the detail() view like so:

urlpatterns = [
    # include will add a file for url mappings for other directories
    path("polls/", include("polls.urls")),
    
    path("admin/", admin.site.urls),
]
