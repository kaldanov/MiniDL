from django.contrib import admin
from .models import Student, Groups, Grades, Teacher, Department, Courses, Files, StudProc, Task, GradesForTask

admin.site.register(Student)
admin.site.register(Grades)
admin.site.register(Groups)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Courses)

#admin.site.register(Deedline)




#admin.site.register(StudProc)

#admin.site.register(Task)
#admin.site.register(GradesForTask)
# Register your models here.
