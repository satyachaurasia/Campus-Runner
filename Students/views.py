from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from accounts.models import Student, Internships, Projects
from django.http import JsonResponse
from datetime import datetime

# Create your views here.


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class ResumeView(View):
    def get(self, request,  *args, **kwargs):
        context=dict()
        context['name'] = request.user.last_name+" "+request.user.first_name
        context['email'] = request.user.email
        context['student'] = Student.objects.get(user=request.user)
        context['projects'] = Projects.objects.filter(student=context['student'])
        context['internships'] = Internships.objects.filter(student=context['student'])
        return render(request, 'resume.html', context)


class SaveInternship(View):
    def post(self, request, *args, **kwargs):
        profile = request.POST.get('profile')
        organization = request.POST.get('organization')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        start_date = datetime.strptime(start_date, '%b %d, %Y').date()
        end_date = datetime.strptime(end_date, '%b %d, %Y').date()

        context = {
            'is_taken':True
        }
        student = Student.objects.get(user=request.user)
        Internships.objects.create(
            student=student,
            profile=profile,
            organization=organization,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        return JsonResponse(context)


class SaveProject(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        start_date = datetime.strptime(start_date, '%b %d, %Y').date()
        end_date = datetime.strptime(end_date, '%b %d, %Y').date()

        context = {
            'is_taken':True
        }
        student = Student.objects.get(user=request.user)
        Projects.objects.create(
            student=student,
            title=title,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        return JsonResponse(context)
