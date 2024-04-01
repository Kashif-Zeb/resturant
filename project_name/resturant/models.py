from django.db import models


# Create your models here.
class Customer(models.Model):
    CustomerID = models.BigAutoField(primary_key=True)
    Customer_name = models.CharField(max_length=70)
    Email = models.EmailField(max_length=70, null=False, unique=True)
    PhoneNumber = models.CharField(max_length=15, null=False, unique=True)


class Reservation(models.Model):
    ReservationID = models.BigAutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Time = models.TimeField()
    Date = models.DateField()
    Number_of_guest = models.PositiveIntegerField()


class Table(models.Model):
    TableID = models.BigAutoField(primary_key=True)
    Capacity = models.PositiveIntegerField(null=False)
    Status = models.CharField(max_length=70)
    ReservationID = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, null=True, blank=True
    )


class Order(models.Model):
    OrderID = models.BigAutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    TableID = models.ForeignKey(Table, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()
    Amount = models.PositiveBigIntegerField()


class MenuItem(models.Model):
    Menu_itemID = models.BigAutoField(primary_key=True)
    ItemName = models.CharField(max_length=70, unique=True, null=False)
    Description = models.TextField(max_length=255)
    Price = models.PositiveBigIntegerField()


class OrderItem(models.Model):
    Order_item_ID = models.BigAutoField(primary_key=True)
    OrderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    Menu_itemID = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
