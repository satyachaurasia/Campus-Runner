from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from accounts.models import Student, Internships, Projects
from django.contrib.auth.models import User

# Create your views here.


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class ResumeView(View):
    def get(self, request,  *args, **kwargs):
        context=dict()
        context['name'] = request.user.last_name+" "+request.user.first_name
        context['email'] = request.user.email
        return render(request, 'resume.html', context)
