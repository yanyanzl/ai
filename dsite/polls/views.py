from django.shortcuts import render

from django.http import HttpResponse


def index1(request):
    return HttpResponse("Hello, world. this is the first page i created!")