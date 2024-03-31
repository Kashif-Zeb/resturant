from rest_framework import serializers
from .models import Customer, Reservation, Table
from .validations import custom_validations as cv


class Serializer_customer(serializers.ModelSerializer):
    CustomerID = serializers.IntegerField(read_only=True)
    Customer_name = serializers.CharField(
        max_length=70, required=True, validators=[cv.validate_customer_name]
    )
    Email = serializers.EmailField(max_length=70, required=True)
    PhoneNumber = serializers.CharField(
        min_length=11, max_length=15, required=True, validators=[cv.PhoneNumber]
    )

    class Meta:
        model = Customer
        fields = ["CustomerID", "Customer_name", "Email", "PhoneNumber"]
        # fields = "__all__"


class Serializer_reservation(serializers.ModelSerializer):
    ReservationID = serializers.IntegerField(read_only=True)
    Time = serializers.TimeField(required=True)
    Date = serializers.DateField(required=True)
    Number_of_guest = serializers.IntegerField(
        required=True, validators=[cv.Number_of_guest]
    )

    class Meta:
        model = Reservation
        fields = ["ReservationID", "CustomerID", "Time", "Date", "Number_of_guest"]


class Reservations_with_customer(serializers.ModelSerializer):
    customer = Serializer_customer(source="CustomerID")

    class Meta:
        model = Reservation
        fields = ["ReservationID", "Time", "Date", "Number_of_guest", "customer"]


class serializer_table(serializers.ModelSerializer):
    TableID = serializers.IntegerField(read_only=True)
    Capacity = serializers.IntegerField(required=True, validators=[cv.Capacity])
    Status = serializers.CharField(required=True, validators=[cv.validate_Status])

    class Meta:
        model = Table
        fields = ["TableID", "Capacity", "Status"]


class serializer_table2(serializers.ModelSerializer):
    Status = serializers.CharField()
    reservation = Reservations_with_customer(source="ReservationID")

    class Meta:
        model = Table
        fields = ["TableID", "Capacity", "Status", "reservation"]


class serializer_update_table(serializers.ModelSerializer):
    ReservationID = serializers.IntegerField(
        required=True,
        validators=[cv.table_reservationid],
    )  # queryset=Reservation.objects.all(),

    Status = serializers.CharField(required=True, validators=[cv.validate_Status])
    Capacity = serializers.IntegerField(required=False)

    class Meta:
        model = Table
        fields = ["TableID", "Capacity", "Status", "ReservationID"]
