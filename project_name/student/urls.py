from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("insert_stu_data/", views.insert_stu_into_db, name="insert_stu_data"),
    path("get_student/", views.get_student, name="get_student"),
]
