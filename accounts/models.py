from django.db import models
from django.contrib.auth.models import User

# Create your models here.
YEAR = (
	('BE', 'Bachelor of Engineering'),
	('TE', 'Third Year'),
	('SE', 'Second Year'),
	('FE', 'First Year')
	)


class College(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name

class Student(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	student_id = models.CharField(max_length=10, blank=True)
	department = models.CharField(max_length=20)
	year = models.CharField(max_length=2, choices=YEAR)
	gpa = models.FloatField()
	phone_number = models.CharField(max_length=10, blank=True, null=True)
	college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
	jobs_applied = models.ManyToManyField('JobProfile', related_name='jobs')

	def __str__(self):
		return self.user.username


class Internships(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False)
	profile = models.CharField(max_length=50)
	organization = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField(blank=True,null=True)
	description = models.TextField(max_length=200, blank=True, null=True)


class Projects(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False)
	title = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	description = models.TextField(max_length=200, blank=True, null=True)


class Faculty(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	department = models.CharField(max_length=20)
	emp_id = models.CharField(max_length=10, unique=True, null=False, blank=False)
	position = models.CharField(max_length=20)
	phone_number = models.CharField(max_length=10, blank=True, null=True)
	college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return self.user.username


class Company(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.company_name


class JobProfile(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=20)
	vacancy = models.PositiveIntegerField()
	job_description = models.TextField(max_length=200)
	criteria = models.PositiveIntegerField(null=True, blank=True)
	college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
