from django.contrib import admin

from .models import Customer, Reservation, Table, Order, OrderItem, MenuItem


# Register your models here.
@admin.register(Customer)
class customer_page(admin.ModelAdmin):
    list_display = ["CustomerID", "Customer_name", "Email", "PhoneNumber"]


@admin.register(Reservation)
class reservation_page(admin.ModelAdmin):
    list_display = ["ReservationID", "CustomerID", "Time", "Date", "Number_of_guest"]


@admin.register(Table)
class table_page(admin.ModelAdmin):
    list_display = ["TableID", "Capacity", "Status", "ReservationID"]


@admin.register(Order)
class order_page(admin.ModelAdmin):
    list_display = ["OrderID", "CustomerID", "TableID", "Date", "Time", "Amount"]


@admin.register(MenuItem)
class menuitem_page(admin.ModelAdmin):
    list_display = ["Menu_itemID", "ItemName", "Description", "Price"]


@admin.register(OrderItem)
class OrderItems_page(admin.ModelAdmin):
    list_display = ["Order_item_ID", "OrderID", "Menu_itemID", "Quantity", "Price"]
