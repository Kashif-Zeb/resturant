from datetime import datetime, timedelta
from functools import wraps
import os 
from django.db import IntegrityError
from django.shortcuts import render
import jwt
from marshmallow import ValidationError
from rest_framework import status,pagination
from rest_framework.decorators import api_view,authentication_classes, permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from django.conf import settings

from .signals import send_login_notification
from .models import Customer, MenuItem, Order, OrderItem, Registration, Reservation, Table
from .serializers import (
    OrderItem_serializer,
    Registration_serializer,
    Serializer_customer,
    Serializer_reservation,
    Reservations_with_customer,
    Serializer_reservation_for_modelsetview,
    get_serializer_order,
    login_serializer,
    serializer_MenuItem,
    serializer_MenuItem2,
    serializer_Order,
    serializer_Update_MenuItem,
    serializer_delete_table,
    serializer_download,
    serializer_table,
    serializer_table2,
    serializer_update_table,
    upload_serializer,
)
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from .tasks import write_order
from rest_framework import viewsets
from rest_framework.decorators import action
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.


def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Token missing'}, status=401)
        try:
            payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
            email = payload['email']
            # Here you can perform additional checks, e.g., verify user existence
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapped_view
@api_view(["POST"])
def registeration(request):
    serializer=Registration_serializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    


def get_tokens_for_user(user):
    refresh = RefreshToken
    refresh = refresh.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def login(request):
    serializer=login_serializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email=serializer.validated_data["Email"]
        password=serializer.validated_data["Password"]
        
        User = Registration.objects.filter(Email=email,Password=password).first() 

        if User is None:  # Checking if user is None
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        # if check_password(password, User.Password):
        #     return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken
        refresh = refresh.for_user(User)
        send_login_notification(sender=None, request=request, user=User)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

        # expiration_time = datetime.utcnow() + timedelta(days=1)  
        # payload = {
        #     'email': email,
        #     'exp': expiration_time  
        # }
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # return JsonResponse({'token': token})
        
        
    else:
        return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(["POST"])
def insert_customer_in_db(request):
    serializer = Serializer_customer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
# @authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
# @jwt_required
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


# class ReservationView(APIView):
@api_view(['GET'])
def get(request):
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
        result = write_order.delay(serial.data)
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
    serializer = serializer_delete_table(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        tid = serializer.validated_data.get("TableID")
        check = Table.objects.filter(TableID=tid).first()
        if check:
            check.delete()
            return Response(
                f"table id {tid} is deleted successfully", status=status.HTTP_200_OK
            )
        else:
            return Response(
                f" table id {tid}  not exist in db", status=status.HTTP_200_OK
            )
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
def get_menuitem(request):
    serializer = serializer_MenuItem2(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        menuid = serializer.validated_data.get("Menu_itemID")
        if menuid:
            aa = MenuItem.objects.filter(Menu_itemID=menuid).first()
            return Response(serializer_MenuItem2(aa).data, status=status.HTTP_200_OK)
        else:
            all = MenuItem.objects.all()
            data = serializer_MenuItem2(all, many=True)
            return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["PUT"])
def update_menu(request):
    serializer = serializer_Update_MenuItem(data=request.data)
    if serializer.is_valid(raise_exception=True):
        Menu_itemID = serializer.validated_data.get("Menu_itemID")
        item = MenuItem.objects.filter(Menu_itemID=Menu_itemID).first()
        if item:
            serializer_data = serializer_Update_MenuItem(
                instance=item, data=serializer.validated_data, partial=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                f"menu_itemID {Menu_itemID} not exist", status=status.HTTP_200_OK
            )
    else:
        Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["DELETE"])
def delete_menu(request):
    serializer = serializer_MenuItem2(data=request.query_params)
    if serializer.is_valid():
        mid = serializer.validated_data.get("Menu_itemID")
        data = MenuItem.objects.filter(Menu_itemID=mid).first()
        if data:
            data.delete()
            return Response(
                f"Menu_ItemID {mid} is deleted successfully", status=status.HTTP_200_OK
            )
        else:
            return Response(
                f" Menu_ItemID {mid} not found",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["POST"])
def create_order(request):
    serializer_class = serializer_Order
    serializer = serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cid = serializer.validated_data.get("CustomerID")
        customer = Customer.objects.filter(CustomerID=cid).first()
        if customer:
            tid = serializer.validated_data.get("TableID")
            reservation = Reservation.objects.filter(CustomerID=cid).first()
            if reservation:
                rid = reservation.ReservationID
                table = Table.objects.filter(TableID=tid, ReservationID=rid).first()
                if table:
                    serializer.create(
                        validated_data={
                            "CustomerID": customer,
                            "TableID": table,
                            "Date": serializer.validated_data.get("Date"),
                            "Time": serializer.validated_data.get("Time"),
                            "Amount": serializer.validated_data.get("Amount"),
                        }
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    f"your table is not exist kindly  do reservation",
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(f"customerid {cid} not found", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
def get_order(request):
    serializer = get_serializer_order(data=request.query_params)
    if serializer.is_valid():
        oid = serializer.validated_data.get("OrderID")
        order = Order.objects.filter(OrderID=oid).first()
        if order:
            return Response(get_serializer_order(order).data, status=status.HTTP_200_OK)
        else:
            return Response(f"orderid {oid} not found", status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["POST"])
def create_orderitem(request):
    serializer_class = OrderItem_serializer
    serializer = serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        oid = serializer.validated_data["OrderID"]
        # orders = Order.objects.filter(OrderID=oid).first()
        if oid:
            menuid = serializer.validated_data["Menu_itemID"]
            # Menu = MenuItem.objects.filter(Menu_itemID=menuid).first()
            if menuid:
                pr = menuid.Price
                qty = serializer.validated_data["Quantity"]
                totalprice = pr * qty

                order_item = serializer.create(
                    validated_data={
                        "OrderID": oid,
                        "Menu_itemID": menuid,
                        "Quantity": qty,
                        "Price": totalprice,
                    }
                )
                # serializer.save(
                #     OrderID=order, Menu_itemID=Menu, Quantity=qty, Price=totalprice
                # )
                new_order_item = OrderItem.objects.get(
                    Order_item_ID=order_item.Order_item_ID
                )

                # Serialize the newly created order item
                serialized_order_item = serializer_class(new_order_item)
                return Response(
                    serialized_order_item.data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    f"menuid {menuid} not found",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                f"order id {oid} not found", status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CustomPagination(pagination.PageNumberPagination):
    page_size = 3  # Set the number of reservations per page
    page_size_query_param = 'page_size'  # Query parameter for page size
    max_page_size = 100
class Reservation_model_set(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = Serializer_reservation_for_modelsetview
    pagination_class = CustomPagination
    # @method_decorator(cache_page(60))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    # def get_queryset(self):
    #     check = cache.get('reservation')
    #     if check is None:
    #         data = Reservation.objects.all()
    #         cache.set('reservation',data,timeout=60)
    #         check = cache.get('reservation')
    #     return check
    # throttle_classes = [UserRateThrottle]
    # @action(detail=False, methods=['post'])
    # def perform_create(self, serializer):
    #     CustomerID = self.request.data.get('CustomerID')
    #     if Customer.objects.filter(pk=CustomerID).exists():
    #         serializer.save()
    #     else:
    #         raise ValidationError({"error": "Customer with provided ID does not exist"})
    # @action(detail=False, methods=['put'])
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     custoemrid=request.data.get("CustomerID")
    #     if Customer.objects.filter(pk=custoemrid).exists():
    #         serializer = self.get_serializer(instance, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response("customer not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # def perform_update(self, request, pk=None):
    #     try:
    #         CustomerID = request.data.get('CustomerID')
    #         if Customer.objects.filter(pk=CustomerID).exists():
    #             instance = self.get_object()
    #             serializer = self.get_serializer(instance, data=request.data)
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()
    #             return Response(serializer.data)
    #     except (ValidationError, PermissionError) as exc:
    #         return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
    # @action(detail=False, methods=['get'])
    # def get_queryset(self):
    #     ReservationID = self.request.query_params.get('ReservationID')
    #     if ReservationID:
    #         queryset = Reservation.objects.filter(ReservationID=ReservationID)
    #     else:
    #         queryset = Reservation.objects.all()
    #     return queryset
    
    # def destroy(self):
    #     ReservationID = self.request.query_params.get('ReservationID')
    #     if ReservationID:
    #         queryset = Reservation.objects.filter(ReservationID=ReservationID)
    #         queryset.delete()
    #         return Response(f"reservation {ReservationID} is deleted successfully",status=status.HTTP_200_OK)


UPLOAD_DIR = 'uploads/'

@api_view(["POST"])
def upload_file(request):
    serializer = upload_serializer(data=request.data)
    if serializer.is_valid():
        user_folder = "userfiles"  # Assuming this is the user folder
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            file_name = uploaded_file.name
            user_dir = os.path.join(UPLOAD_DIR, user_folder)
            os.makedirs(user_dir, exist_ok=True)  # Create user folder if it doesn't exist
            file_path = os.path.join(user_dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return Response(f"Your file {file_name} is uploaded successfully", status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(["GET"])
def download_file(request):
    serializer = serializer_download(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        user_folder = "userfiles"
        user_dir = os.path.join(UPLOAD_DIR,user_folder)
        file_path = os.path.join(user_dir, serializer.validated_data.get("filename"))
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)