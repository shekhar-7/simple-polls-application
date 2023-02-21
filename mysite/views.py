from django.http import HttpResponseRedirect
from django.urls import reverse


def index(req):
    return HttpResponseRedirect(reverse('polls:index'))
