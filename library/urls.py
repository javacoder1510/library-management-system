from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Students
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path(
        "students/edit/<int:id>/",
        views.edit_student,
        name="edit_student"
    ),
    path(
        "students/delete/<int:id>/",
        views.delete_student,
        name="delete_student"
    ),

    # Teachers
    path("teachers/", views.teachers, name="teachers"),
    path("teachers/add/", views.add_teacher, name="add_teacher"),
    path(
        "teachers/edit/<int:id>/",
        views.edit_teacher,
        name="edit_teacher"
    ),
    path(
        "teachers/delete/<int:id>/",
        views.delete_teacher,
        name="delete_teacher"
    ),

    # Books
    path("books/", views.books, name="books"),
    path("books/add/", views.add_book, name="add_book"),
    path(
        "books/edit/<int:id>/",
        views.edit_book,
        name="edit_book"
    ),
    path(
        "books/delete/<int:id>/",
        views.delete_book,
        name="delete_book"
    ),

    # Issue / Return
    path("issued-books/", views.issued_books, name="issued_books"),
    path("issue-book/", views.issue_book, name="issue_book"),
    path(
        "return-book/<int:id>/",
        views.return_book,
        name="return_book"
    ),
]
