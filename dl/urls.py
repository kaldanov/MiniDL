from django.urls import path
from . import views

app_name = "dl"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.check_account, name='check_account'),
    path('grades/', views.grades, name='grades'),
    path('grades/<int:course_id>', views.grades_detail, name='grades_detail'),
    path('course/course_id=<int:courses_id>', views.courses, name='courses'),
    path('course/course_id=<int:courses_id>/add_task', views.add_task_menu, name='add_task_menu'),
    path('course/course_id=<int:courses_id>/add_task/task_id=<int:task_id>', views.add_task_student, name='add_task_student'),
    path('course/course_id=<int:courses_id>/add_task/add', views.add_task, name='add_task'),



    path('course/course_id=<int:courses_id>/task_id=<int:task_id>', views.show_task, name='show_task'),
    path('course/course_id=<int:courses_id>/<int:author_id>', views.upload_file, name='upload_file'),
    path('course/course_id=<int:courses_id>/attendance', views.for_attendance, name='for_attendance'),
    path('course/course_id=<int:course_id>/rate/group_id=<int:group_id>/task_id=<int:task_id>', views.rate, name='rate'),
    path('rate/<int:course_id>/<int:group_id>/<int:teacher_id>/<int:student_id>/<int:task_id>', views.set_grade, name='set_grade'),
    path('course/search', views.search_course, name='search_course'),
    path('profile/<int:user_id>', views.see_profile, name='see_profile'),
    path('profile/<int:user_id>/change_photo', views.change_photo, name='change_photo')
    #path('courses/', views.teacher_courses, name='courses')
    #path('groups/', views.all_groups, name='all_groups'),
    #path('group_id=<int:group_id>', views.index, name='index'),
    #path('student_id=<int:student_id>', views.show_subjects, name='show_subjects'),
    #path('<int:student_id>/<int:subject_id>/', views.get_grade, name='get_grade'),
]