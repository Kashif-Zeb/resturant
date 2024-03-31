from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import Serializer_student
from django.http import HttpResponse, JsonResponse

# Create your views here.


@api_view(["POST"])
def insert_stu_into_db(request):
    serializer = Serializer_student(data=request.data)
    if serializer.is_valid():
        serializer.save()
        aa = Student.objects.get()
        print(aa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(
            serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


@api_view(["GET"])
def get_student(request):
    try:
        stuid = request.query_params.get("stuid")
        student = Student.objects.get(stuid=stuid)
    except Student.DoesNotExist:
        return JsonResponse(
            {"error": "Student with stuid {} does not exist".format(stuid)}, status=404
        )
    student_data = {
        "stuid": student.stuid,
        "name": student.name,
        "email": student.email,
        "number": student.number,
    }
    return JsonResponse(student_data)
