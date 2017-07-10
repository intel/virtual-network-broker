from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class MgmtUIView(TemplateView):
    """
    Class to Manage the frontend UI rendering
    """
    print("inside MgmtUIView")
    template_name = 'index.html'


