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
