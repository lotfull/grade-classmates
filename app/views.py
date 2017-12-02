from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import StudentEnrolled

def main_page(request):
    return HttpResponse("Main Page")

def index(request):
    time_now = timezone.now()
    context = {'time_now': time_now}
    return render(request, 'app/index.html', context)

def dashboard(request):
    current_user = request.user

    context = {'courses_enrolled':[], 'first_name': current_user.first_name,
               'last_name': current_user.last_name, 'email': current_user.email,
               'meeting_enrolled':[]}

    students_enrolled = StudentEnrolled.objects.all()
    for student_enrolled in students_enrolled:
        if student_enrolled.student.user == current_user:
            course_info = {'course_name': student_enrolled.course.name, 'start_date': student_enrolled.course.start_date,
                           'end_date': student_enrolled.course.end_date }
            context.get('courses_enrolled').append(course_info)

    print(current_user, 'enters in dashboard')

    return render(request, 'app/dashboard.html', context)