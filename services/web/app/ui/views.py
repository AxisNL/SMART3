import json
import os.path

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.http import Http404
from django.conf import settings
from django.conf import settings
from django.contrib.auth.decorators import login_required


#@login_required
def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))

#
# @login_required
# def hypervisors(request):
#     template = loader.get_template('hypervisors.html')
#     datastore = os.path.join(settings.BASE_DIR, 'hypervisors.json')
#     with open(datastore, 'r') as f:
#         hypervisor_list = json.load(f)
#     hypervisor_list = sorted(hypervisor_list, key=lambda d: d['sort'])
#     context = {
#         'hypervisor_list': hypervisor_list
#     }
#     return HttpResponse(template.render(context, request))
