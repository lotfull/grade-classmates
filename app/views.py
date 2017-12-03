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


from .models import Meeting, GradeAction, TeacherAttends, StudentAttends
from django.shortcuts import get_object_or_404


def meeting_results(request, meeting_id):
    current_user = request.user
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    teachers = TeacherAttends.objects.filter(meeting_id=meeting_id)  # TODO unique
    students =  StudentAttends.objects.filter(meeting_id=meeting_id)
    teachers_names = [teacher.teacher.user.username for teacher in teachers]
    students_names = [student.student.user.username for student in students]
    participants_names = teachers_names + students_names

    grades = GradeAction.objects.filter(meeting_id=meeting_id)
    mapping_from_username_to_index = {username: index
                                     for index, username in enumerate(participants_names)}

    table_of_grades = [[None] * (len(participants_names) + 1) for _ in range(len(participants_names) + 1)]
    for grade in grades:
        try:
            index_grading = mapping_from_username_to_index[grade.grading.username]
            index_graded = mapping_from_username_to_index[grade.graded.username]
            table_of_grades[index_grading + 1][index_graded + 1] = grade.grade
        except (IndexError, KeyError) as e:
            pass
            # TODO grade action from where grading or graded is not in meeting

    table_of_grades[0][0] = ""
    for i in range(len(participants_names)):
        table_of_grades[0][i + 1] = participants_names[i]
        table_of_grades[i + 1][0] = participants_names[i]

    context = {
        'meeting': meeting,
        'grades': table_of_grades,
    }
    print(context)
    return render(request, 'app/vote_results_for_participant.html', context)


from django.contrib.auth.models import User
from .models import Merit


def meeting_vote_choice(request, meeting_id, graded_id):
    current_user = request.user
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    graded = get_object_or_404(User, pk=graded_id)  # TODO Check that graded is from meeting_id
    merits = Merit.objects.all()
    merits_names_positive = list(map(lambda merit: merit.name, list(filter(lambda merit: merit.description == '+', merits))))
    merits_names_negative = list(map(lambda merit: merit.name, list(filter(lambda merit: merit.description == '-', merits))))

    context = {
        'meeting': meeting,
        'grading': current_user,
        'graded': graded,
        'merits_positive': merits_names_positive,
        'merits_negative': merits_names_negative
    }
    return render(request, 'app/vote_choice.html', context)  # TODO Nikita


from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def meeting_vote_action(request, meeting_id, graded_id):
    current_user = request.user
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    graded = get_object_or_404(User, pk=graded_id)
    try:
        grade = request.POST['grade']
        del request.POST['grade']
        merits_ids = request.POST.keys()
    except KeyError:
        merits = Merit.objects.all()
        merits_names_positive = list(
            map(lambda merit: merit.name,
                list(filter(lambda merit: merit.description == '+', merits))))
        merits_names_negative = list(
            map(lambda merit: merit.name,
                list(filter(lambda merit: merit.description == '-', merits))))
        context = {
            'meeting': meeting,
            'grading': current_user,
            'graded': graded,
            'merits_positive': merits_names_positive,
            'merits_negative': merits_names_negative
        }
        return render(request, 'app/vote_choice.html', context)
    else:
        for merit_id in merits_ids:
            merit = Merit.objects.get(pk=merit_id)
            grade_action, created = GradeAction.objects.get_or_create(
                grading=current_user,
                graded=graded,
                grade=grade,
                merit=merit,
                meeting=meeting
            )
            grade_action.save()
        return HttpResponseRedirect(reverse('meetings_results', args=(meeting_id,)))
