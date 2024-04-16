from rest_framework import serializers
from .models import Customer, Order, OrderItem, Registration, Reservation, Table, MenuItem
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


class serializer_MenuItem(serializers.ModelSerializer):
    Menu_itemID = serializers.IntegerField(read_only=True)
    ItemName = serializers.CharField(
        required=True, max_length=70, validators=[cv.ItemName]
    )
    Description = serializers.CharField(required=True, max_length=255)
    Price = serializers.IntegerField(required=True, validators=[cv.Price])

    class Meta:
        model = MenuItem
        fields = "__all__"


class serializer_MenuItem2(serializers.ModelSerializer):
    Menu_itemID = serializers.IntegerField(required=False)

    class Meta:
        model = MenuItem
        fields = "__all__"
        read_only_fields = ["ItemName", "Description", "Price"]


class serializer_delete_table(serializers.ModelSerializer):
    TableID = serializers.IntegerField(required=True)

    class Meta:
        model = Table
        fields = ["TableID"]


class serializer_Update_MenuItem(serializers.ModelSerializer):
    Menu_itemID = serializers.IntegerField(required=True)
    ItemName = serializers.CharField(
        required=True, max_length=70, validators=[cv.ItemName]
    )
    Description = serializers.CharField(required=True, max_length=255)
    Price = serializers.IntegerField(required=True, validators=[cv.Price])

    class Meta:
        model = MenuItem
        fields = "__all__"  # exclude = ['users']


class serializer_Order(serializers.ModelSerializer):
    OrderID = serializers.IntegerField(read_only=True)
    CustomerID = serializers.IntegerField(required=True, validators=[cv.CustomerID])
    TableID = serializers.IntegerField(required=True, validators=[cv.TableID])
    Date = serializers.DateField(required=True)
    Time = serializers.TimeField(required=True)
    Amount = serializers.IntegerField(required=True, validators=[cv.Amount])

    class Meta:
        model = Order
        fields = "__all__"


class get_serializer_order(serializers.ModelSerializer):
    OrderID = serializers.IntegerField(required=True)
    Table = serializer_table2(source="TableID", required=False)
    Date = serializers.DateField(required=False)
    Time = serializers.TimeField(required=False)
    Amount = serializers.IntegerField(
        required=False,
    )

    class Meta:
        model = Order
        fields = [
            "OrderID",
            "Date",
            "Time",
            "Amount",
            "Table",
        ]


class OrderItem_serializer(serializers.ModelSerializer):
    # Order_item_ID = serializers.IntegerField(read_only=True)
    OrderID = serializers.DjangoModelField(validators=[cv.OrderID])
    Menu_itemID = serializers.DjangoModelField(validators=[cv.Quantity])
    Quantity = serializers.IntegerField(required=True, validators=[cv.Quantity])
    # Price = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ["Order_item_ID", "OrderID", "Menu_itemID", "Quantity", "Price"]
        read_only_fields = ("Order_item_ID", "Price")

    # def create(self, validated_data):
    #     print("Validated Data:", validated_data)
    #     try:
    #         order_id = validated_data["OrderID"]  # Accessing the primary key
    #         order = Order.objects.get(OrderID=order_id)
    #         menu_id = validated_data["Menu_itemID"]  # Accessing the primary key
    #         menu = MenuItem.objects.get(Menu_itemID=menu_id)
    #         qty = validated_data["Quantity"]
    #         price = menu.Price * qty
    #         order_item = OrderItem.objects.create(
    #             OrderID=order.OrderID,
    #             Menu_itemID=menu.Menu_itemID,
    #             Quantity=qty,
    #             Price=price,
    #         )
    #         return super().create(validated_data)
    #     except Order.DoesNotExist:
    #         raise serializers.ValidationError("Invalid Order reference")
    #     except MenuItem.DoesNotExist:
    #         raise serializers.ValidationError("Invalid MenuItem reference")

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response["Order_item_ID"] = instance.Order_item_ID
    #     response["Price"] = instance.Price
    #     return response

    # write_only_fields = ("Price",)

    # read_only_fields = ('is_active', 'is_staff')
    # extra_kwargs = {
    #     'security_question': {'write_only': True},
    #     'security_question_answer': {'write_only': True},
    #     'password': {'write_only': True}
    # }


class Registration_serializer(serializers.ModelSerializer):
    Regid=serializers.IntegerField(read_only=True)
    Firstname=serializers.CharField(max_length=50)
    Lastname=serializers.CharField(max_length=50)
    Email=serializers.EmailField(max_length=50)
    Password=serializers.CharField(max_length=50)
    # Token=serializers.CharField(read_only=True)
    class Meta:
        model = Registration
        fields = ["Regid","Firstname","Lastname","Email","Password"]



class login_serializer(serializers.Serializer):
    Email=serializers.EmailField(max_length=50)
    Password=serializers.CharField(max_length=50)
    Token=serializers.CharField(read_only=True)