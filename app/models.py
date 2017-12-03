from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Merit(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class MeetingType(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Meeting(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'course {}; meeting_type {}; date {}; place {}'.format(
            self.course, self.meeting_type, self.date, self.place)


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
        if created:
            print("created", teacherTeaches)
        else:
            print("existing", teacherTeaches)
        teacherTeaches.save()


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
        if created:
            print("created", studentEnrolled)
        else:
            print("existing", studentEnrolled)
        studentEnrolled.save()


class TeacherAttends(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.teacher, self.meeting)


class StudentAttends(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.student, self.meeting)


class GradeAction(models.Model):
    grading = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_grading')
    graded = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_graded')
    grade = models.IntegerField()
    merit = models.ForeignKey(Merit, on_delete=models.SET_NULL, blank=True, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'grading {}; graded {}; grade {}; merit {}; meeting {}'.format(
            self.grading, self.graded, self.grade, self.merit, self.meeting)

class DataManager(models.Manager):

    users_names = ["Fadeev", "Terentyev", "Kozlov", "Kuzmin", "Fedorov", "Shcherbakov", "Dmitriev", "Yudin", "Belousova", "Gerasimov", "Seleznyov", "Prokhorov", "Bobrov", "Birds", "Crane", "Zuyev", "Karpov", "Vladimir", "Kolobov", "Nesterov", "Kondratyev", "Petrov", "Sparrows", "Maksimov", "Isayev", "Frolov", "Shchukin", "Alexander", "Tretyakov", "Vorontsov", "Kosheleva", "Efimova", "Lobanov", "Sorokin", "Belousova", "Boer", "Seleznyov", "Sukhanov", "Morozov", "Doronin", "Vorob", "Makarov", "Nesterov", "Sokolov", "Beetles", "Nekrasov", "Gavrilov", "Wings", "Simonov", "Myasnikova", "Cossacks", "Sparrows", "Kovalev", "Ermakova", "Larionov", "Vorob", "Sokolov", "Mironov", "Davidoff", "Loginova", "Zhdanov", "Bobylev", "Subbotina", "Dorofeev", "Popova", "Voronova", "Index", "Guryev", "Karpov", "Zhdanov", "Orlov", "Kulikova", "Sharova", "Ignatova", "Myasnikov", "Boar", "Panov", "Mammoth", "O", "Bykov", "Panova", "Belousova", "Gushchin", "Koshelev", "Krasilnikov", "Fomin", "Danilov", "Savel", "Pancakes", "Vlasov", "Mikhaylov", "Smith", "Pavlov", "Ponomareva", "Nesterov", "Mikheev", "Frolov", "Konovalov", "Kirillov", "Kolesnikov"]

    courses_names = ["Algebra", "Algorithms and data structures", "Algorithms and data structures", "Analysis of markets and competitiveness", "English", "computer Architecture and operating systems", "Safety", "Introduction to object-oriented programming", "Introductory research seminar", "Discrete mathematics", "Discrete mathematics ", "Discrete optimization", "Differential equations, History, Linear algebra and geometry", "macroeconomics", "Mathematical analysis", "Machine learning 1", "Machine learning on big data", "Interdisciplinary course work", "Microeconomics", "research seminar in Distributed systems", "Scientific seminar", "Independent English exam ", "Continuous optimization, Parallel and distributed computing", "Software project", "Project Software project 1", "Psychology in it", "Theory of databases", "Theory of probability and mathematical statistics", "Teaching", "Teaching practice", "Physical culture"]

    @staticmethod
    def generate_data():
        for i, name in enumerate(DataManager.users_names):
            user, created = User.objects.get_or_create(
                username=name, email=name+'@edu.hse.ru')
            if created:
                user.set_password(name)
                user.save()
                if (i % 20 == 0):
                    User_Role = Teacher
                else:
                    User_Role = Student
                user_role = User_Role()
                user_role.user = user
                user_role.save()

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
            course, created = Course.objects.get_or_create(
                name=course_name,
                description="The course of {} give student basic skills in {}"
                    .format(course_name, course_name),
                start_date=start_date,
                end_date=end_date,
            )
            if created:
                print("created", course)
            else:
                print("existing", course)
            course.save()

    @staticmethod
    def connect_students_teachers_to_courses():
        students = Student.objects.all()
        teachers = Teacher.objects.all()
        courses = Course.objects.all()
        for course in courses:
            num_students_per_course = random.randint(15, 30)
            few_students = random.sample(students, num_students_per_course)
            teacher = random.choice(teachers)
            for student in few_students:
                StudentEnrolled.create(course, student)
            TeacherTeaches.create(course, teacher)
