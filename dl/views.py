from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from .models import Student, Groups, Grades, Teacher, Department, Courses, StudProc, Files, Task, GradesForTask, StudentFilesForTask
import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage


def home(request):
    teachers_list = {}
    kek = {}
    kek.update(csrf(request))
    tasks = ""
    if request.user.is_authenticated:
        try:
            if request.user.teacher:
                courses_list = Courses.objects.all().filter(teacher=request.user.teacher.pk).order_by('subject_name')

            else:
                return redirect('/')

        except Teacher.DoesNotExist:
            if request.user.student:
                courses_list = Courses.objects.all().filter(department=request.user.student.group.group_dep).order_by('subject_name')
                teachers_list = Teacher.objects.all()
                tasks = Task.objects.all().filter(groups=request.user.student.group).order_by('date2')
            else:
                return redirect('/')
        kek = {
            'teachers_list': teachers_list,
            'courses_list': courses_list,
            'user': auth.get_user(request),
            'tasks': tasks
        }
    return render(request, 'main.html', kek)


def check_account(request): # prover9et account
    args = {}
    args.update(csrf(request))

    if not request.user.is_authenticated:
        if request.POST:
            login = request.POST['enter_login']
            password = request.POST['enter_pass']
            user = auth.authenticate(username=login, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                args['login_error'] = "Login or password is incorrect!"
                return render(request, 'login.html', args)
        else:
            return render(request, 'login.html', args)
    else:
        auth.logout(request)
        return redirect('/')


def grades(request):
    courses_list = Courses.objects.all().filter(department=request.user.student.group.group_dep).order_by('subject_name')
    grades_list = Grades.objects.all().filter(student__user__username=request.user.username).order_by('-date')

    kek = {
        'grades_list': grades_list,
        'courses_list': courses_list,
        'student': auth.get_user(request)
    }

    return render(request, 'grades.html', kek)


def grades_detail(request, course_id):
    tasks_list = Task.objects.all().filter(course_id=course_id).order_by('title')

    try:
        grade = GradesForTask.objects.all().filter(course_id=course_id, student_id=request.user.student.pk).order_by('-date')
    except:
        grade = 0

    course_id = course_id
    course_name = Courses.objects.filter(pk=course_id).get().subject_name
    kek = {
        'grades_list': grade,
        'tasks_list': tasks_list,
        'student': auth.get_user(request),
        'course_id': course_id,
        'course_name': course_name
    }

    return render(request, 'gradedetail.html', kek)



def courses(request, courses_id): #bazadan alad course
    context = {}
    group_id = ""
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

    groups_list = Groups.objects.all().filter(group_dep__courses=courses_id)
    files_list = Files.objects.all().filter(course_id=courses_id)
    tasks_list = Task.objects.all().filter(course_id=courses_id)
    timenow = timezone.now()
    weeks = []
    for i in range(1,16):
        weeks.append(i)

    try:
        course_name = Courses.objects.get(pk=courses_id).subject_name
    except:
        raise Http404("Course not found!")

    kek = {
        'group_id': group_id,
        'date': timenow,
        'tasks_list': tasks_list,
        'files_list': files_list,
        'course_name': course_name,
        'weeks': weeks,
        'groups_list': groups_list,
        'course_id': courses_id,
        'context': context,
    }

    return render(request, 'course.html', kek)


def see_profile(request, user_id): #function
    s_user = " "
    t_user = " "
    courses_list = []

    try:
        if request.user.teacher:
            if Student.objects.filter(user_id=user_id).exists():
                s_user = Student.objects.get(user_id=user_id).user
                courses_list = Courses.objects.all().filter(department=s_user.student.group.group_dep).order_by('subject_name')
        else:
            return redirect('/')

    except:
        if request.user.student:
            if Teacher.objects.filter(user_id=user_id).exists():
                t_user = Teacher.objects.get(user_id=user_id).user
                courses_list = Courses.objects.all().filter(teacher__user_id=user_id).order_by('subject_name')
        else:
            return redirect('/')
    kek = {
        'student': s_user,
        'teacher': t_user,
        'courses_list': courses_list
    }
    return render(request, 'profile.html', kek)


def change_photo(request, user_id): # s pomoshyu etoi func mojno menyat foto
    try:
        if request.user.student:
            user = Student.objects.get(user_id=user_id)
            user.image = request.FILES['file']
            user.save()

    except:
        if request.user.teacher:
            user = Teacher.objects.get(user_id=user_id)
            user.image = request.FILES['file']
            user.save()

    return HttpResponseRedirect(reverse('dl:see_profile', args=(user_id,)))

def rate(request, course_id, group_id, task_id):
    grades_list = GradesForTask.objects.all().filter(course_id=course_id, task_id=task_id).order_by('-date')
    students_list = Student.objects.all().filter(group_id=group_id)
    group_name = Groups.objects.get(pk=group_id).group_name
    task = Task.objects.get(pk=task_id)
    course_id = course_id
    course_name = Courses.objects.get(pk=course_id).subject_name
    files_list = StudentFilesForTask.objects.filter(student__group=group_id)
    kek = {
        'grades_list': grades_list,
        'students_list': students_list,
        'course_id': course_id,
        'group_name': group_name,
        'course_name': course_name,
        'task': task,
        'files_list': files_list
    }
    return render(request, 'rate.html', kek)


def set_grade(request, course_id, group_id, teacher_id, student_id, task_id):
    message = ''
    if request.method == 'POST':
        course = Courses.objects.get(pk=course_id)
        group = Groups.objects.get(pk=group_id)
        teacher = Teacher.objects.get(user_id=teacher_id)
        student = Student.objects.get(pk=student_id)
        task = Task.objects.get(pk=task_id)
        newGrade = int(request.POST['inputGrade'])
        #email = student.user.email
        try:
            grade = GradesForTask.objects.get(course_id=course_id, group_id=group_id, teacher_id=teacher_id, student_id=student_id,task_id=task_id)
            grade.grade = newGrade
            grade.save()

            message = 'You take ' + str(newGrade) +'!/n'+ 'Course: ' + course.subject_name + './n' + 'Task title: ' + task.title
            send_mail('DLite | You have rated!', message, 'theswtrwthr@gmail.com', ['said.ur@mail.ru'], fail_silently=False)
        except:
            grade = GradesForTask()
            grade.course = course
            grade.group = group
            grade.student = student
            grade.teacher = teacher
            grade.grade = newGrade
            grade.task = task
            grade.save()
            message = 'You take ' + str(
                newGrade) + '!/n' + 'Course: ' + course.subject_name + './n' + 'Task title: ' + task.title
            send_mail('DLite | You have rated!', message, 'theswtrwthr@gmail.com', ['said.ur@mail.ru'],
                      fail_silently=False)

    else:
        raise Http404("wdadw not found!")

    return HttpResponseRedirect(reverse('dl:rate', args=(course_id, group_id,task_id)))


def search_course(request): #func kotoraya iwet studenta v glavnom liste
    if request.method == "POST":
        try:
            courses_list = Courses.objects.all().filter(subject_name__contains=request.POST['name'], teacher=request.user.teacher).order_by('subject_name')
            course_size = len(courses_list)
        except:
            courses_list = Courses.objects.all().filter(subject_name__contains=request.POST['name'],department=request.user.student.group.group_dep ).order_by('subject_name')
            course_size = len(courses_list)
    else:
        raise Http404("не найдено!")

    return render(request, 'main.html',
                  {'courses_list': courses_list,
                   'course_size': course_size})

def for_attendance(request, courses_id):
    studproc = StudProc.objects.filter(course_id=courses_id)
    course_name = Courses.objects.get(pk = courses_id)
    kek = {
        'studproc': studproc,
        'course_name': course_name,
        'course_id': courses_id
    }

    return render(request, 'attendance.html', kek)


def upload_file(request,courses_id,author_id): # func kotoraya ska4ivaet file
    title = request.POST['title']
    uploaded_file = request.FILES['file']
    new_author_id = Teacher.objects.get(pk=author_id)
    new_course_id = Courses.objects.get(pk=courses_id)
    week = request.POST['week']
    files = Files()
    files.file = uploaded_file
    files.author = new_author_id
    files.week = week
    files.title = title
    files.course = new_course_id
    files.save()


    return HttpResponseRedirect(reverse('dl:courses', args=(courses_id,)))


def add_task_menu(request, courses_id):
    groups = Groups.objects.filter(group_dep__courses=courses_id)
    course_name = Courses.objects.get(pk=courses_id).subject_name
    course_id = courses_id
    # course_name = Courses.objects.get(id=courses_id).subject_name
    # course_id = courses_id
    return render(request, 'addtask.html',{'groups':groups,'course_id':course_id,'course_name':course_name})


def add_task(request, courses_id):
    if request.method == "POST":
        title = request.POST['title']
        week = request.POST['week']
        info = request.POST['info']
        date1 = request.POST['date1_date'] + " " + request.POST['date1_time']
        date2 = request.POST['date2_date'] + " " + request.POST['date2_time']
        groups = request.POST.getlist('groups')

        # info = request.POST['info']
        # date1 = request.POST['date1_date'] + " " + request.POST['date1_time']
        # date2 = request.POST['date2_date'] + " " + request.POST['date2_time']
        # groups = request.POST.getlist('groups')
        uploaded_file = ""
        if request.FILES:
            uploaded_file = request.FILES['file']
        new_course_id = Courses.objects.get(pk=courses_id)

        tasks = Task()
        tasks.file = uploaded_file
        tasks.week = week
        tasks.title = title
        tasks.info = info
        tasks.course = new_course_id
        tasks.date1 = date1
        tasks.date2 = date2
        tasks.save()
        for i in groups:
            groups_list = Groups.objects.get(group_name=i).pk
            tasks.groups.add(groups_list)
        tasks.save()

    if request.method == 'GET':
        return render(request, 'main.html')
    return HttpResponseRedirect(reverse('dl:courses', args=(courses_id,)))


def show_task(request, courses_id, task_id):
    try:
        grade = GradesForTask.objects.all().filter(course_id=courses_id, task_id=task_id,student_id=request.user.student.pk).order_by('-date')[:1].get()
    except:
        grade = 0
    groups_list = Groups.objects.all().filter(group_dep__courses=courses_id)
    course_id = courses_id
    course_name = Courses.objects.get(pk=courses_id).subject_name
    task = Task.objects.get(pk=task_id)
    date = timezone.now()
    x = date.replace(microsecond=0)
    myFile = ""

    # course_name = Courses.objects.get(pk=courses_id).subject_name
    # task = Task.objects.get(pk=task_id)
    # date = timezone.now()
    # x = date.replace(microsecond=0)
    # myFile = ""


    try:
        if request.user.student:
            myFile = StudentFilesForTask.objects.filter(student=request.user.student)
    except:
        myFile = ""
    if date > task.date2:
        newDate = x - task.date2.replace(microsecond=0)
    elif date < task.date2:
        newDate = task.date2.replace(microsecond=0) - x
    kek = {
        'task': task,
        'course_name': course_name,
        'course_id': course_id,
        'date': date,
        'newDate': newDate,
        'groups_list': groups_list,
        'myFile': myFile,
        'grade': grade
    }
    return render(request, 'taskpage.html',kek)


def add_task_student(request, courses_id, task_id):
    if request.method == "POST":
        student = Student.objects.get(pk=request.user.student.pk)
        task = Task.objects.get(pk=task_id)
        uploaded_file = request.FILES['file']
        file = StudentFilesForTask()
        file.student = student
        file.task = task
        file.file = uploaded_file
        file.save()

        return HttpResponseRedirect(reverse('dl:show_task', args=(courses_id, task_id,)))


def set_attendance(request, group_id, course_id):
    return render(request, 'student.html')