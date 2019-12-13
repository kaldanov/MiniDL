from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Courses(models.Model):  # It's course where admin can add subjects
    class Meta:
        db_table = "courses"

    subject_name = models.CharField(max_length=200)

    def __str__(self):
        id = str(self.pk)
        return self.subject_name + " | " + id


class Teacher(models.Model):  # Role: Teacher of course
    class Meta:
        db_table = "teachers"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses)
    image = models.ImageField(upload_to='profiles_images', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.user.username


class Department(models.Model):  #klass kotoraya rasprodil9et kafedru stdenta
    class Meta:
        db_table = "departments"

    department_name = models.CharField(max_length=80)
    courses = models.ManyToManyField(Courses)

    def __str__(self):
        return self.department_name


class Groups(models.Model): #klass v kotorom studenty rasprodel9yutsya po gruppam
    class Meta:
        db_table = "groups"

    group_dep = models.ForeignKey(Department, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class Student(models.Model):
    class Meta:
        db_table = "students"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles_images', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.user.username


class Grades(models.Model): #class v kotorom mojno stavit otsenki
    class Meta:
        db_table = "grades"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.student.user.first_name + " " + self.student.user.last_name + " | " + self.course.subject_name


class Files(models.Model):
    class Meta:
        db_table = 'files'

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField()

    def __str__(self):
        return self.title


class Task(models.Model):
    class Meta:
        db_table = 'tasks'

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    info = models.TextField(max_length=300)
    file = models.FileField(upload_to='files/tasks', blank=True)
    week = models.IntegerField()
    date1 = models.DateTimeField()
    date2 = models.DateTimeField()
    groups = models.ManyToManyField(Groups)

    def __str__(self):
        return self.course.subject_name + " | " + self.title


class StudProc(models.Model):
    class Meta:
        db_table = 'studproc'

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    CHOICES = (
        ('PRACTICE', 'PRACTICE'),
        ('LECTURE', 'LECTURE')
    )
    type = MultiSelectField(choices=CHOICES)
    room = models.IntegerField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.subject_name + " | " + str(self.room)


class GradesForTask(models.Model):
    class Meta:
        db_table = "task_grades"

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.course.subject_name + " | " + self.task.title


class StudentFilesForTask(models.Model):
    class Meta:
        db_table = "students_files"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/student', blank=True)

    def __str__(self):
        return self.student.user.first_name + " " + self.student.user.last_name + " | " + self.task.title
