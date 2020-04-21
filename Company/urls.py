"""campusrunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import JobView, JobPost,JobDetailView, SeeResume
from django.contrib.auth.decorators import login_required

app_name = 'company'


urlpatterns = [
    path('jobs/', login_required(JobView.as_view()), name='jobs'),
    path('jobs/<str:job_id>/', login_required(JobDetailView.as_view()), name='jobss'),
    path('job-post/', login_required(JobPost.as_view()), name='job_post'),
    path('see-resume/<str:student_id>/', login_required(SeeResume.as_view()), name='see_resume'),


]
