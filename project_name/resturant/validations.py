from django.http import JsonResponse
from rest_framework import serializers


class custom_validations:
    @staticmethod
    def PhoneNumber(value):
        if value is None:
            raise serializers.ValidationError("Phone number cannot be left empty")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")

    @staticmethod
    def validate_customer_name(value):
        if value is None:
            raise serializers.ValidationError("Customer name cannot be left empty")
        if not value.isalpha():
            raise serializers.ValidationError(
                "Customer name should contain only alphabets"
            )

    @staticmethod
    def Number_of_guest(value):
        if value is None:
            raise serializers.ValidationError(f"Number of guest cantnot be left empty")
        if value <= 0:
            raise serializers.ValidationError(
                "Number of guest must be in positive integer and greater than zero"
            )

        if not isinstance(value, int):
            raise serializers.ValidationError("Number of guests must be an integer.")

    @staticmethod
    def Capacity(value):
        if value is None:
            raise serializers.ValidationError("Capacity cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError(
                "Number of guest must be in positive integer and greater than zero"
            )
        if not isinstance(value, int):
            raise serializers.ValidationError("Number of guests must be an integer.")

    @staticmethod
    def validate_Status(value):
        if value is None:
            raise serializers.ValidationError("Capacity cannot be left empty")
        if value not in ["Available", "Reserved"]:
            raise serializers.ValidationError(
                "Status must be either 'Available' or 'Reserved'"
            )

    @staticmethod
    def table_reservationid(value):
        if value is None:
            raise serializers.ValidationError("ReservationID cannot be left empty")
        # if not isinstance(value, int):
        #     raise serializers.ValidationError(
        #         "ReservationID must be a positive integer"
        #     )
        if value <= 0:
            raise serializers.ValidationError(
                "ReservationID must be a positive integer"
            )

    @staticmethod
    def ItemName(value):
        if value is None:
            raise serializers.ValidationError("ItemName cannot be left empty")
        if not value.isalpha():
            raise serializers.ValidationError("ItemName must contains alphabets only")

    @staticmethod
    def Price(value):
        if value is None:
            raise serializers.ValidationError("ReservationID cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError(
                "ReservationID must be a positive integer"
            )

        if isinstance(value, float) and value != int(value):
            raise serializers.ValidationError("Float values are not allowed.")

    @staticmethod
    def CustomerID(value):
        if value is None:
            raise serializers.ValidationError("CustomerID cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("CustomerID must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("CustomerID must be a positive integer")

    @staticmethod
    def TableID(value):
        if value is None:
            raise serializers.ValidationError("TableID cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("TableID must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("TableID must be a positive integer")

    @staticmethod
    def Amount(value):
        if value is None:
            raise serializers.ValidationError("Amount cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("Amount must be a positive integer")

    @staticmethod
    def Quantity(value):
        if value is None:
            raise serializers.ValidationError("Quantity cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be a positive integer")

    @staticmethod
    def Menu_itemID(value):
        if value is None:
            raise serializers.ValidationError("Menu_itemID cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("Menu_itemID must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("Menu_itemID must be a positive integer")

    @staticmethod
    def OrderID(value):
        if value is None:
            raise serializers.ValidationError("OrderID cannot be left empty")
        if value <= 0:
            raise serializers.ValidationError("OrderID must be a positive integer")

        if not isinstance(value, int):
            raise serializers.ValidationError("OrderID must be a positive integer")
