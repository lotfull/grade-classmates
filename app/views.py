from collections import Counter
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import GradeAction, StudentAttends, StudentEnrolled

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

    students_attended = StudentAttends.objects.all()
    for student_attended in students_attended:
        if student_attended.student.user == current_user:
            meeting = student_attended.meeting
            meeting_info = {}
            meeting_info['date'] = meeting.date
            meeting_info['place'] = meeting.place
            meeting_info['course'] = meeting.course
            meeting_info['meeting_type'] = meeting.meeting_type
            context.get('meeting_enrolled').append(meeting_info)

    grade_actions = GradeAction.objects.all().filter(graded = current_user)
    context['positive_qualities'] = {}
    context['negative_qualities'] = {}
    for grade in grade_actions:
        merit = grade.merit
        if merit.description == '+':
            if context['positive_qualities'].get(merit.name) == None:
                context['positive_qualities'][merit.name] = 1
            else:
                context['positive_qualities'][merit.name] += 1
        else:
            if context['negative_qualities'].get(merit.name) == None:
                context['negative_qualities'][merit.name] = 1
            else:
                context['negative_qualities'][merit.name] += 1

    for i in context['positive_qualities'].items():
        print(i[0], i[1])

    return render(request, 'app/dashboard.html', context)