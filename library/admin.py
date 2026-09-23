from django.contrib import admin
from .models import Student, Teacher, Book, IssuedBook


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Book)
admin.site.register(IssuedBook)
