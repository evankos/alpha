from django.shortcuts import render
from django.views.generic import TemplateView


class FrontendView(TemplateView):
    template_name = 'app.html'


