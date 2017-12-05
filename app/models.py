from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import random

def save_if(model, created):
    if created:
        print("created", model)
        model.save()
    else:
        print("existing", model)

models.Model.save_if = save_if

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()

    @staticmethod
    def create(user):
        student, created = Student.objects.get_or_create(
            user=user
        )
        save_if(student, created)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()

    @staticmethod
    def create(user):
        teacher, created = Teacher.objects.get_or_create(
            user=user
        )
        save_if(teacher, created)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create(name, description, start_date, end_date):
        course, created = Course.objects.get_or_create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        save_if(course, created)


class Merit(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create(name, description):
        merit, created = Merit.objects.get_or_create(
            name=name,
            description=description
        )
        save_if(merit, created)


class MeetingType(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    @staticmethod
    def create(description):
        meeting_type, created = MeetingType.objects.get_or_create(
            description=description
        )
        save_if(meeting_type, created)


class Meeting(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'course {}; meeting_type {}; date {}/{}/{}; place {}'.format(
            self.course, self.meeting_type, self.date.day, self.date.month, self.date.year, self.place)

    @staticmethod
    def create(date, place, course, meeting_type):
        meeting, created = Meeting.objects.get_or_create(
            date=date,
            place=place,
            course=course,
            meeting_type=meeting_type
        )
        save_if(meeting, created)


class TeacherTeaches(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.teacher, self.course)

    @staticmethod
    def create(course, teacher):
        teacherTeaches, created = TeacherTeaches.objects.get_or_create(
            course = course,
            teacher = teacher
        )
        save_if(teacherTeaches, created)


class StudentEnrolled(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.student, self.course)

    @staticmethod
    def create(course, student):
        studentEnrolled, created = StudentEnrolled.objects.get_or_create(
            course = course,
            student = student
        )
        save_if(studentEnrolled, created)


class TeacherAttends(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.teacher, self.meeting)

    @staticmethod
    def create(meeting, teacher):
        teacherAttends, created = TeacherAttends.objects.get_or_create(
                meeting = meeting,
                teacher = teacher
            )
        save_if(teacherAttends, created)


class StudentAttends(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.student, self.meeting)

    @staticmethod
    def create(meeting, student):
        studentAttends, created = StudentAttends.objects.get_or_create(
                meeting = meeting,
                student = student
            )
        save_if(studentAttends, created)


class GradeAction(models.Model):
    grading = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_grading')
    graded = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_graded')
    grade = models.IntegerField()
    merit = models.ForeignKey(Merit, on_delete=models.SET_NULL, blank=True, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'grading {}; graded {}; grade {}; merit {}; meeting {}'.format(
            self.grading, self.graded, self.grade, self.merit, self.meeting)

    @staticmethod
    def create(grading, graded, grade, merit, meeting):
        gradeAction, created = GradeAction.objects.get_or_create(
            grading=grading,
            graded=graded,
            grade=grade,
            merit=merit,
            meeting=meeting
        )
        save_if(gradeAction, created)

class DataManager(models.Manager):

    users_names = ["Fadeev", "Terentyev", "Kozlov", "Kuzmin", "Fedorov", "Shcherbakov", "Dmitriev", "Yudin", "Belousova", "Gerasimov", "Seleznyov", "Prokhorov", "Bobrov", "Birds", "Crane", "Zuyev", "Karpov", "Vladimir", "Kolobov", "Nesterov", "Kondratyev", "Petrov", "Sparrows", "Maksimov", "Isayev", "Frolov", "Shchukin", "Alexander", "Tretyakov", "Vorontsov", "Kosheleva", "Efimova", "Lobanov", "Sorokin", "Belousova", "Boer", "Seleznyov", "Sukhanov", "Morozov", "Doronin", "Vorob", "Makarov", "Nesterov", "Sokolov", "Beetles", "Nekrasov", "Gavrilov", "Wings", "Simonov", "Myasnikova", "Cossacks", "Sparrows", "Kovalev", "Ermakova", "Larionov", "Vorob", "Sokolov", "Mironov", "Davidoff", "Loginova", "Zhdanov", "Bobylev", "Subbotina", "Dorofeev", "Popova", "Voronova", "Index", "Guryev", "Karpov", "Zhdanov", "Orlov", "Kulikova", "Sharova", "Ignatova", "Myasnikov", "Boar", "Panov", "Mammontov", "Lotfullin", "Bykov", "Panova", "Belousova", "Gushchin", "Koshelev", "Krasilnikov", "Fomin", "Danilov", "Savel", "Pancakes", "Vlasov", "Mikhaylov", "Smith", "Pavlov", "Ponomareva", "Nesterov", "Mikheev", "Frolov", "Konovalov", "Kirillov", "Kolesnikov"]

    courses_names = ["Algebra", "Algorithms and data structures", "Algorithms and data structures", "Analysis of markets and competitiveness", "English", "computer Architecture and operating systems", "Safety", "Introduction to object-oriented programming", "Introductory research seminar", "Discrete mathematics", "Discrete mathematics ", "Discrete optimization", "Differential equations, History, Linear algebra and geometry", "macroeconomics", "Mathematical analysis", "Machine learning 1", "Machine learning on big data", "Interdisciplinary course work", "Microeconomics", "research seminar in Distributed systems", "Scientific seminar", "Independent English exam ", "Continuous optimization, Parallel and distributed computing", "Software project", "Project Software project 1", "Psychology in it", "Theory of databases", "Theory of probability and mathematical statistics", "Teaching", "Teaching practice", "Physical culture"]

    meeting_types_descriptions = ["lecture", "seminar"]

    merit_names_descriptions = [("communication skills", "+"), ("ability to admit a mistake", "+"), ("intellect", "+"), ("open-minded", "+"), ("responsibility", "+"), ("overall", "+")]

    places = ["kochna, 610", "kochna, 229", "kochna, 330", "kochna, 203", "kochna, 408", "kochna, 306", "kochna, 505", "kochna, 432", "kochna, 521", "kochna, 200", "kochna, 223", "kochna, 607", "kochna, 319", "kochna, 211", "kochna, 221", "kochna, 404", "kochna, 413", "kochna, 317", "kochna, 234", "kochna, 504"]

    @staticmethod
    def generate_test_data():
        DataManager.print_all_users_roles()
        DataManager.generate_students_teachers(num_of_users=35)
        DataManager.generate_courses()
        DataManager.generate_studentEnrolled_teacherTeaches()
        DataManager.generate_meeting_types()
        DataManager.generate_merits()
        DataManager.generate_meetings(weeks_number=5)
        DataManager.generate_students_teachers_attends()
        DataManager.generate_grade_actions()

    @staticmethod
    def generate_students_teachers(num_of_users=None, every_nth_is_teacher=20):
        num_of_users = min(num_of_users, len(DataManager.users_names))
        few_users = DataManager.users_names[:num_of_users]
        for i, name in enumerate(few_users):
            user, created = User.objects.get_or_create(
                username=name, email=name+'@edu.hse.ru')
            if created:
                user.set_password(name)
                user.save()
                if (i % every_nth_is_teacher == 0):
                    Teacher.create(user)
                else:
                    Student.create(user)
            else:
                print("existing", user)

    @staticmethod
    def print_all_users_roles():
        stud_n, teach_num, nobody_n = 0, 0, 0
        for user in User.objects.all():
            user_is_student = False
            for student in Student.objects.all():
                if student.user == user:
                    print(user, "is student")
                    user_is_student = True
                    break
            if user_is_student:
                stud_n += 1
                continue
            user_is_teacher = False
            for teacher in Teacher.objects.all():
                if teacher.user == user:
                    print(user, "is teacher")
                    user_is_teacher = True
                    break
            if user_is_teacher:
                teach_num += 1
                continue
            print(user, "is NOBODY")
            nobody_n += 1
        print("stud_n = {}, teach_num = {}, nobody_n = {}"
              .format(stud_n, teach_num, nobody_n))

    @staticmethod
    def generate_courses():
        courses_num = 5
        students_per_course = 20
        start_date = datetime(2017, 9, 1)
        end_date = datetime(2018, 6, 30)
        few_courses_names = random.sample(DataManager.courses_names, 5)
        for i, course_name in enumerate(few_courses_names):
            course_description = "The course of {} give student basic skills in {}".format(course_name, course_name)
            Course.create(course_name, course_description, start_date, end_date)

    @staticmethod
    def generate_studentEnrolled_teacherTeaches():
        students = list(Student.objects.all())
        teachers = Teacher.objects.all()
        courses = Course.objects.all()
        for course in courses:
            students_per_course = min(30, len(students))
            num_students_per_course = random.randint(students_per_course/2, students_per_course)
            few_students = random.sample(students, num_students_per_course)
            teacher = random.choice(teachers)
            for student in few_students:
                StudentEnrolled.create(course, student)
            TeacherTeaches.create(course, teacher)

    @staticmethod
    def generate_meeting_types():
        for meeting_type_description in DataManager.meeting_types_descriptions:
            MeetingType.create(meeting_type_description)

    @staticmethod
    def generate_merits():
        for (name, description) in DataManager.merit_names_descriptions:
            Merit.create(name, description)

    @staticmethod
    def generate_meetings(meetings_per_week=1, places=places, courses=Course.objects.all(), meeting_types=MeetingType.objects.all(), weeks_number=54):
        for course in courses:
            print(course)
            meeting_date = course.start_date + relativedelta(day=random.randint(1, 4))
            place = random.choice(places)
            print(place)
            meeting_type = random.choice(meeting_types)
            print(meeting_type)
            number_of_weeks = min(((course.end_date - meeting_date).days / 7), weeks_number)
            number_of_meetings = meetings_per_week*number_of_weeks
            print(number_of_meetings)
            for index in range(number_of_meetings):
                meeting_date += relativedelta(days=7)
                Meeting.create(meeting_date, place, course, meeting_type)

    @staticmethod
    def generate_students_teachers_attends(courses=Course.objects.all()):
        for course in courses:
            course_meetings = Meeting.objects.filter(course=course)
            course_studentsEnrolled = StudentEnrolled.objects.filter(course=course)
            course_teachersEnrolled = TeacherTeaches.objects.filter(course=course)
            for meeting in course_meetings:
                for studentEnrolled in course_studentsEnrolled:
                    StudentAttends.create(meeting, studentEnrolled.student)
                for teacherEnrolled in course_teachersEnrolled:
                    TeacherAttends.create(meeting, teacherEnrolled.teacher)

    @staticmethod
    def generate_grade_actions(meetings=Meeting.objects.all(),
                               courses=Course.objects.all(),
                               merits=Merit.objects.all(),
                               grading_proportion=1./3):

        merits_without_overall = list(filter((lambda x: x.name != "overall"), merits))
        overall_merit = list(filter((lambda x: x.name=="overall"), merits))[0]
        for meeting in meetings:
            studentsAttends = StudentAttends.objects.filter(meeting=meeting)
            teachersAttends = TeacherAttends.objects.filter(meeting=meeting)
            users = list(map((lambda x: x.student.user), studentsAttends))
            users += list(map((lambda x: x.teacher.user), teachersAttends))
            sample_size = int(len(users)*grading_proportion)
            grading_users = random.sample(users, sample_size)
            for grading_user in grading_users:
                graded_users = random.sample(users, sample_size)
                for graded_user in graded_users:
                    if grading_user == graded_user:
                        continue
                    merits_number = random.randint(1, len(merits_without_overall))
                    merits_sample = random.sample(merits_without_overall, merits_number)
                    overall_grade = 0
                    for merit in merits_sample:
                        grade = random.randint(1, 10)
                        overall_grade += grade
                        GradeAction.create(grading_user, graded_user, grade, merit, meeting)
                    overall_grade /= merits_number
                    GradeAction.create(grading_user, graded_user, overall_grade, overall_merit, meeting)


    links = [
        ["Dashboard", "/app/dashboard/"],
        ["Students Login", "/accounts/login/"],
        ["Admin Login", "/admin/login/"],
        ["Meeting 1 all results", "/meeting/1/results/"],
        ["Meeting 1 vote choice", "/meeting/1/vote_choice/1"],
        ["Meeting 1 vote action", "/meeting/1/vote_action/1"],
        ["Logout", "/accounts/logout/"],
        ["Main", "/"]
    ]

    @staticmethod
    def generate_links():
        for link in DataManager.links:
            Link.create(link[0], link[1])

class Link(models.Model):
    name = models.CharField(max_length=200)
    ref = models.CharField(max_length=200)

    def __str__(self):
        return self.name + "-" + self.ref

    @staticmethod
    def create(name, ref):
        link, created = Link.objects.get_or_create(
            name=name,
            ref=ref
        )
        save_if(link, created)














