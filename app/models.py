from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()


class Merit(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)


class MeetingType(models.Model):
    description = models.CharField(max_length=50)


class Meeting(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL)
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.SET_NULL)


class TeacheTeaches(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class StudentEnrolled(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class TeacherAttends(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)


class StudentAttends(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)


class GradeAction(models.Model):
    grading = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField()
    merit = models.ForeignKey(Merit, on_delete=models.SET_NULL)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL)
