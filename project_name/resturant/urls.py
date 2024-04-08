from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("insert_cust_data/", views.insert_customer_in_db, name="insert_customer_data"),
    path("get_cust/", views.get_cust_data, name="get_cust"),
    path("update_cust/", views.update_cust, name="update customer"),
    path("delete_cust/", views.delete_cust, name="Delete Customer"),
    path("inset_reservation/", views.create_reservation, name="inserting reservations"),
    path(
        "get_reservation/",
        views.ReservationView.as_view(),
        name="get single and all both",
    ),
    path("update_revervation/", views.update_reservation, name="update reservation"),
    path("delete_reservation/", views.delete_reservation, name="Delete reservation"),
    path("create_table/", views.create_table, name="create table"),
    path("get_table/", views.get_tables, name="get table"),
    path("update_table/", views.update_table, name="update table"),
    path("delete_table/", views.delete_table, name="delete table"),
    path("create_menuitem/", views.create_menuitem, name="create menuitem"),
    path("get_menuitem/", views.get_menuitem, name="get menuitem"),
    path("update_menuitem/", views.update_menu, name="update menuitem"),
    path("delete_menuitem/", views.delete_menu, name="delete menuitem"),
    path("create_order/", views.create_order, name="create order"),
    path("get_order/", views.get_order, name="get order"),
    path("create_orderitem/", views.create_orderitem, name="create orderitem"),
]
