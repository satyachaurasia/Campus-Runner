from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from accounts.models import Student, Internships, Projects, JobProfile
from django.http import JsonResponse
from datetime import datetime

# Create your views here.


class RegisterForJob(View):
    def get(self, request, *args, **kwargs):
        try:
            job_id = request.GET.get('job_id')
            job = JobProfile.objects.get(id=job_id)
            student = Student.objects.get(user=request.user)
            student.jobs_applied.add(job)

            context = {
                'success': True
            }
        except Exception as e:
            print(e)
            context = {
                'success': False
            }

        return JsonResponse(context)



class EligibleJobs(View):
    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        context = dict()
        already_applied = student.jobs_applied.all().values('id')
        context['job_list'] = JobProfile.objects.filter(college=student.college, criteria__lte=student.gpa).exclude(id__in=already_applied)

        return render(request,'ApplyJobs.html', context)


class Dashboard(View):
    template_name = "dashboard.html"
    def get(self, request, *args, **kwargs):
        context = dict()
        student = Student.objects.get(user=request.user)
        context['job_applied'] = student.jobs_applied.all()
        return render(request, 'dashboard.html', context)



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
