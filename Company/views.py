from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, View
from accounts.models import JobProfile, Company, College, Projects, Internships, Student
from django.http import JsonResponse

# Create your views here.

class SeeResume(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs['student_id']
        student = get_object_or_404(Student, pk=student_id)
        context = dict()
        context['name'] = student.user.last_name + " " + student.user.first_name
        context['email'] = student.user.email
        context['projects'] = Projects.objects.filter(student=student)
        context['internships'] = Internships.objects.filter(student=student)
        return render(request,'student_resume.html',context)





class JobDetailView(View):
    def get(self, request, *args, **kwargs):
        job_id = kwargs['job_id']
        context = dict()
        job = JobProfile.objects.get(id=job_id)
        context['job'] = job
        context['applied_student'] = job.jobs.all()
        return render(request, 'JobDetail.html', context)

class JobView(View):
    def get(self,request, *args, **kwargs):
        context = dict()
        company = Company.objects.get(user=request.user)
        context['job_profiles'] = JobProfile.objects.filter(company=company).order_by('-id')
        context['college_list'] = College.objects.all()
        return render(request, 'jobs.html', context)


class JobPost(View):
    def post(self, request, *args, **kwargs):
        job_title = request.POST.get('job_title')
        vacancy = request.POST.get('vacancy')
        job_description = request.POST.get('job_description')
        criteria = request.POST.get('criteria')
        college_id = request.POST.get('college')

        company = Company.objects.get(user=request.user)
        college = College.objects.get(id=college_id)

        try:
            JobProfile.objects.create(
                job_title=job_title,
                vacancy=vacancy,
                job_description=job_description,
                criteria=criteria,
                college=college,
                company=company
            )
            context = {
                'success': True,
                'job_title': job_title,
                'vacancy': vacancy,
                'job_description':job_description,
                'criteria':criteria,
                'college':college.name,
            }
        except Exception as e:
            print(e)
            context = {
                'success': False
            }

        return JsonResponse(context)

