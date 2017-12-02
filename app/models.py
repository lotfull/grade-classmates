from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


class Merit(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50, null=True)


class MeetingType(models.Model):
    description = models.CharField(max_length=50)


class Meeting(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=50, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.SET_NULL, null=True)


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
    grading = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_grading')
    graded = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_graded')
    grade = models.IntegerField()
    merit = models.ForeignKey(Merit, on_delete=models.SET_NULL, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True)
