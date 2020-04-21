from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from accounts.models import Student, Faculty, Company, College
from django.contrib.auth import authenticate, logout,login

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if Student.objects.filter(user=user).exists():
                return redirect('students:dashboard')
            elif Faculty.objects.filter(user=user).exists():
                return redirect('students:dashboard')
            else:
                return redirect('company:jobs')
        else:
            context = {
                'no_success': True
            }

            return render(request, "login.html", context)


class SignupView(View):
    def get(self, request, *args, **kwargs):
        context = dict()
        context['college_list'] = College.objects.values('id', 'name')

        return render(request, "signup.html", context)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        account_type = request.POST.get('account_type')

        if account_type:
            try:
                user = User.objects.create_user(username=email,
                                                email=email,
                                                password=password,
                                                first_name = first_name,
                                                last_name = last_name)
            except Exception as e:
                print(e)

        if account_type == 'student' and user:
            student_id = request.POST.get('student_id')
            department = request.POST.get('department')
            gpa = request.POST.get('gpa')
            year = request.POST.get('year')
            college_id = request.POST.get('college')

            try:
                college = College.objects.get(id=college_id)
                Student.objects.create(user=user,
                                      student_id=student_id,
                                      department=department,
                                      year=year,
                                      gpa=gpa,
                                      phone_number=phone,
                                      college=college)
                context = {
                    'success': True
                }
                return render(request, "signup.html", context)
            except Exception as e:
                print(e)
        elif account_type == 'faculty' and user:
            emp_id = request.POST.get('emp_id')
            position = request.POST.get('position')
            faculty_department = request.POST.get('faculty_department')
            college_id = request.POST.get('college')
            try:
                college = College.objects.get(id=college_id)
                Faculty.objects.create(user=user,
                                       department=faculty_department,
                                       emp_id=emp_id,
                                       position = position,
                                       phone_number=phone,
                                       college=college
                                       )
                context = {
                    'success': True
                }
                return render(request, "signup.html", context)
            except Exception as e:
                print(e)
        elif account_type=='company' and user:
            company = request.POST.get('company')
            try:
                Company.objects.create(
                    user=user,
                    company_name=company,
                    phone_number = phone,
                )
                context = {
                    'success': True
                }
                return render(request, "signup.html", context)
            except Exception as e:
                print(e)

        context = {
            'no_success': True
        }

        return render(request, "signup.html", context)
