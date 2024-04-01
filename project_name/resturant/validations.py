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
