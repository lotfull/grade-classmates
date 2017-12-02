from django.contrib import admin

from . import models as app_models
admin.site.register(app_models.Student)
admin.site.register(app_models.Teacher)

admin.site.register(app_models.Course)
admin.site.register(app_models.Merit)

admin.site.register(app_models.MeetingType)
admin.site.register(app_models.Meeting)

admin.site.register(app_models.TeacherTeaches)
admin.site.register(app_models.StudentEnrolled)

admin.site.register(app_models.TeacherAttends)
admin.site.register(app_models.StudentAttends)

admin.site.register(app_models.GradeAction)


