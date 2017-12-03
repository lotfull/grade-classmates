from django.db import models
from django.contrib.auth.models import User

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


class StudentEnrolled(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.student, self.course)


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
        print("stud_n = {}, teach_num = {}, nobody_n = {}".format(stud_n, teach_num, nobody_n))
