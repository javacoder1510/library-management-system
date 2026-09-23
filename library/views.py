from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Student, Teacher, Book, IssuedBook


# Dashboard
def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "teacher_count": Teacher.objects.count(),
        "book_count": Book.objects.count(),
        "issued_count": IssuedBook.objects.filter(status="Issued").count(),
    }
    return render(request, "library/dashboard.html", context)


# Students
def students(request):
    data = Student.objects.all().order_by("-id")
    return render(request, "library/students.html", {"students": data})


def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            class_name=request.POST["class_name"],
        )
        return redirect("students")

    return render(request, "library/student_form.html")


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST["name"]
        student.email = request.POST["email"]
        student.phone = request.POST["phone"]
        student.class_name = request.POST["class_name"]
        student.save()

        return redirect("students")

    return render(
        request,
        "library/student_form.html",
        {"student": student}
    )


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("students")


# Teachers
def teachers(request):
    data = Teacher.objects.all().order_by("-id")
    return render(request, "library/teachers.html", {"teachers": data})


def add_teacher(request):
    if request.method == "POST":
        Teacher.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            department=request.POST["department"],
        )
        return redirect("teachers")

    return render(request, "library/teacher_form.html")


def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        teacher.name = request.POST["name"]
        teacher.email = request.POST["email"]
        teacher.phone = request.POST["phone"]
        teacher.department = request.POST["department"]
        teacher.save()

        return redirect("teachers")

    return render(
        request,
        "library/teacher_form.html",
        {"teacher": teacher}
    )


def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    return redirect("teachers")


# Books
def books(request):
    data = Book.objects.all().order_by("-id")
    return render(request, "library/books.html", {"books": data})


def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            name=request.POST["name"],
            author=request.POST["author"],
            category=request.POST["category"],
            quantity=request.POST["quantity"],
        )
        return redirect("books")

    return render(request, "library/book_form.html")


def edit_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.name = request.POST["name"]
        book.author = request.POST["author"]
        book.category = request.POST["category"]
        book.quantity = request.POST["quantity"]
        book.save()

        return redirect("books")

    return render(
        request,
        "library/book_form.html",
        {"book": book}
    )


def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect("books")


# Issued Books
def issued_books(request):
    data = IssuedBook.objects.select_related(
        "book", "student", "teacher"
    ).order_by("-id")

    return render(
        request,
        "library/issued_books.html",
        {"issued_books": data}
    )


def issue_book(request):
    books_data = Book.objects.filter(quantity__gt=0)
    students_data = Student.objects.all()
    teachers_data = Teacher.objects.all()

    if request.method == "POST":

        book = get_object_or_404(
            Book,
            id=request.POST["book"]
        )

        student_id = request.POST.get("student")
        teacher_id = request.POST.get("teacher")

        student = (
            Student.objects.get(id=student_id)
            if student_id
            else None
        )

        teacher = (
            Teacher.objects.get(id=teacher_id)
            if teacher_id
            else None
        )

        if not student and not teacher:
            return render(
                request,
                "library/issue_form.html",
                {
                    "books": books_data,
                    "students": students_data,
                    "teachers": teachers_data,
                    "error": "Please select Student or Teacher."
                }
            )

        IssuedBook.objects.create(
            book=book,
            student=student,
            teacher=teacher,
        )

        book.quantity -= 1
        book.save()

        return redirect("issued_books")

    return render(
        request,
        "library/issue_form.html",
        {
            "books": books_data,
            "students": students_data,
            "teachers": teachers_data,
        }
    )


def return_book(request, id):
    issued = get_object_or_404(IssuedBook, id=id)

    if issued.status == "Issued":
        issued.status = "Returned"
        issued.return_date = timezone.now().date()
        issued.save()

        issued.book.quantity += 1
        issued.book.save()

    return redirect("issued_books")
