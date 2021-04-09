from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

# Create your views here.
class ResultView(TemplateView):
    template_name = 'letter/index.html'
