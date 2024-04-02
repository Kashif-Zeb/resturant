from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Reservation, Table
from .serializers import (
    Serializer_customer,
    Serializer_reservation,
    Reservations_with_customer,
    serializer_table,
    serializer_table2,
    serializer_update_table,
)
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView


# Create your views here.


@api_view(["POST"])
def insert_customer_in_db(request):
    serializer = Serializer_customer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
def get_cust_data(request):
    cid = request.query_params.get("id")
    if cid is not None:
        customer = Customer.objects.get(CustomerID=cid)
        if customer is not None:
            data = Serializer_customer(customer).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Error": "No data"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    else:
        customers = Customer.objects.all().order_by("-CustomerID")
        data = Serializer_customer(customers, many=True).data
        return Response(data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_cust(request):
    cid = request.data.get("CustomerID")
    customer = Customer.objects.filter(CustomerID=cid).first()
    if customer is not None:
        serializer = Serializer_customer(customer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    else:
        return Response("Customer does not exist", status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_cust(request):
    if "id" in request.query_params:
        cid = request.query_params.get("id")
        if cid is not None:
            if cid.isdigit():
                cust = Customer.objects.filter(CustomerID=cid).first()
                if cust is not None:
                    cust.delete()
                    return Response(
                        f"customer {cid} is deleted successfully ",
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        f"customer {cid} not found", status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    "id must be a positive integer",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                "id cannot be left empty", status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    else:
        return Response(
            "id is required filed ", status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


@api_view(["POST"])
def create_reservation(request):
    serializer = Serializer_reservation(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ReservationView(APIView):
    def get(self, request):
        rid = request.query_params.get("Rid")
        if rid is not None:
            if rid.isdigit():
                reservation = Reservation.objects.filter(ReservationID=rid).first()
                if reservation:
                    serial = Reservations_with_customer(reservation)
                    return Response(
                        serial.data,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        f"Reservation with ID {rid} does not exist.",
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                return Response(
                    "Rid must be a positive integer.",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        else:
            reservation = Reservation.objects.all()
            serial = Reservations_with_customer(reservation, many=True)
            return Response(serial.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_reservation(request):
    rid = request.data.get("ReservationID")
    reservation = Reservation.objects.filter(ReservationID=rid).first()
    if reservation:
        serialier = Serializer_reservation(reservation, data=request.data, partial=True)
        if serialier.is_valid(raise_exception=True):
            serialier.save()
            return Response(serialier.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serialier.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    else:
        return Response(f"reservation {rid} nof found", status=status.ok)


@api_view(["DELETE"])
def delete_reservation(request):
    if "ReservationID" in request.query_params:
        rid = request.query_params.get("ReservationID")
        if rid:
            if rid.isdigit():
                reservation = Reservation.objects.filter(ReservationID=rid).first()
                if reservation is not None:
                    reservation.delete()
                    return Response(
                        f"{rid} is deleted successfully ", status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        f"{rid} not found  in db", status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    "ReservationID myst be a positive integer",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                "ReservationID cannot be left empty",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
    else:
        return Response(
            "ReservationID is requried", status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


@api_view(["POST"])
def create_table(request):
    serializer = serializer_table(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
def get_tables(request):
    if "status" in request.query_params:
        statuses = request.query_params["status"]
        if statuses:
            if statuses.isalpha():
                serializer_table = Table.objects.filter(Status__icontains=statuses)
                if serializer_table:
                    serialize_data = serializer_table2(serializer_table, many=True).data
                    return Response(serialize_data, status=status.HTTP_200_OK)
                else:
                    return Response("data not found", status=status.HTTP_200_OK)

            else:
                return Response(
                    "status contains alphabets only",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                "status cannot be left empty",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
    else:
        return Response(
            "status is requried", status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


# @api_view(["PUT"])
# def update_table(request):
#     # if "ReservationID" and "Status" in request.data:
#     ReservationID = request.data.get("ReservationID")
#     reservation = Reservation.objects.filter(ReservationID=ReservationID).first()
#     if reservation:
#         no_of_guest = reservation.Number_of_guest
#         table = Table.objects.filter(Status="Available", Capacity=no_of_guest).first()
#         if table:
#             serializer = serializer_update_table(
#                 instance=table, data=request.data, partial=True
#             )
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(
#                     serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
#                 )
#         else:
#             return Response(
#                 "table is not available right now plz wait",
#                 status=status.HTTP_200_OK,
#             )

#     else:
#         return Response("reservationid not found", status=status.HTTP_200_OK)


# else:
#     if "ReservationID" not in request.data:
#         return Response(
#             "reservationid is required", status=status.HTTP_422_UNPROCESSABLE_ENTITY
#         )
#     else:
#         return Response(
#             "status is required", status=status.HTTP_422_UNPROCESSABLE_ENTITY
#         )


@api_view(["PUT"])
def update_table(request):
    # breakpoint()
    serializer_class = serializer_update_table

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        ReservationID = serializer.validated_data.get("ReservationID")
        reservation = Reservation.objects.filter(ReservationID=ReservationID).first()
        if reservation:
            no_of_guest = reservation.Number_of_guest
            table = Table.objects.filter(
                Status="Available", Capacity=no_of_guest
            ).first()
            if table:
                serializer.update(
                    table,
                    validated_data={
                        "ReservationID": reservation,
                        "Status": serializer.validated_data.get("Status"),
                    },
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No available table found", status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                "Reservation ID not found", status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["POST"])
def create_menuitem(request):
    if request.method == "POST":
        serializer = serializer_MenuItem(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "Item with this name already exists."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


@api_view(["DELETE"])
def delete_table(request):
    serializer=serializer_delete_table(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        tid=serializer.validated_data.get("TableID")
        check=Table.objects.filter(TableID=tid).first()
        if check:
            check.delete()
            return Response(f"table id {tid} is deleted successfully",status=status.HTTP_200_OK)
        else:
            return Response(f" table id {tid}  not exist in db",status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)