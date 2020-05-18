from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Menu_Pizza, Menu_Pasta, Menu_Sub, Menu_Topping, Menu_Salad, Menu_Dinner_Platter, Menu_Extra, Orders, All_Orders
from django.contrib import messages
import smtplib
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    context = {
        "user": request.user,
        "menu_pizzas":     Menu_Pizza.objects.all(),
        "menu_toppings": Menu_Topping.objects.values("name"),
        "menu_subs": Menu_Sub.objects.all(),
        "menu_extras": Menu_Extra.objects.all(),
        "menu_pastas": Menu_Pasta.objects.all(),
        "menu_salads": Menu_Salad.objects.all(),
        "menu_dinner_platters": Menu_Dinner_Platter.objects.all(),
    }

    special = "Pepperoni, Spinach, Ham, Onions"
    context["special"] = special

    try:
        order = Orders.objects.get(user=request.user, status="Initiated")
    except:
        order = Orders(user=request.user)
        order.save()
    cart = All_Orders.objects.filter(user=request.user, order_id=order.pk)
    count = 0
    for item in cart:
        count += 1
    context["count"] = count

    return render(request, "orders/index.html", context)


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.filter(email=email)
        if len(user) != 0:
            return render(request, "orders/register.html", {"message": "Oops! Email already exist. Try another email."})

        user = User.objects.filter(username=username)
        if len(user) != 0:
            return render(request, "orders/register.html", {"message": "Oops! Username already exist. Try another username."})

        user = User.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password,
        )
        user.save()
        print("userrr=====", user)

        return render(request, "orders/login.html", {"message": "Your account has been successfully created!"})

    else:
        return render(request, "orders/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Oops! Username/password is incorrect."})

    else:
        return render(request, "orders/login.html", {"message": None})


def logout_user(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "You are currently logged out!"})


def add_item_view(request):
    name = request.POST["name"]
    item_price = float(request.POST["item_price"])
    size = request.POST["size"]

    try:
        special = request.POST["special"]
    except:
        special = ""

    extras = special
    try:
        extra1 = request.POST["extra1"]
    except:
        extra1 = ""
    try:
        extra2 = request.POST["extra2"]
    except:
        extra2 = ""
    try:
        extra3 = request.POST["extra3"]
    except:
        extra3 = ""
    try:
        extra4 = request.POST["extra4"]
    except:
        extra4 = ""

    if len(extra1) != 0:
        extras += f"{extra1}"
    if len(extra2) != 0:
        extras += f"{extra2}"
    if len(extra3) != 0:
        extras += f"{extra3}"
    if len(extra4) != 0:
        extras += f"{extra4}"

    length = len(extras)
    try:
        if extras[length - 1] == ",":
            extras = extras[:-1]
    except:
        extras = ""

    extras = extras.replace(",", ", ")

    try:
        price1 = float(request.POST["price1"])
    except:
        price1 = 0.00
    try:
        price2 = float(request.POST["price2"])
    except:
        price2 = 0.00
    try:
        price3 = float(request.POST["price3"])
    except:
        price3 = 0.00
    try:
        price4 = float(request.POST["price4"])
    except:
        price4 = 0.00

    price_extra = price1 + price2 + price3 + price4
    item_price += price_extra
    item_cart = name

    if len(size) != 0:
        item_cart += f" ({size})"

    user = request.user
    order = Orders.objects.get(user=user, status="Initiated")
    order_id = order.id
    cart = All_Orders(user=user, order_id=order_id,
                      order_item=item_cart, extras=extras, item_price=item_price,)
    cart.save()

    order.total_order = float(order.total_order) + item_price
    order.save()

    messages.success(request, "Item just added!")
    return HttpResponseRedirect(reverse("index"))


def cart_item_view(request):
    order = Orders.objects.get(user=request.user, status="Initiated")
    cart = All_Orders.objects.filter(user=request.user, order_id=order.pk)
    count = 0

    for item in cart:
        count += 1

    context = {
        "cart": cart,
        "count": count,
        "total_order": order.total_order,
        "order_id": order.id,
    }

    return render(request, "orders/cart.html", context)


def remove_order_view(request):
    item_id = request.POST["item_id"]
    item_price = request.POST["item_price"]
    user = request.user
    cart = All_Orders.objects.filter(id=item_id).delete()

    order = Orders.objects.get(user=user, status="Initiated")
    order.total_order = float(order.total_order) - float(item_price)
    order.save()

    messages.success(request, "You just removed item!")
    return HttpResponseRedirect(reverse("cart_item"))


def place_order_view(request):
    order = Orders.objects.get(user=request.user, status="Initiated")
    cart = All_Orders.objects.filter(
        user=request.user, order_id=order.pk).all()
    order.status = "Has been completed"
    order.save()

    # Personal touch : Send email confirmation

    sender = "pinocchiospizza1987@gmail.com"
    request.user.email
    recipient = request.user.email

    message = f"""
    You have been successfully purchased from PinocchioPizza!
    Your order:

        """

    for item in cart:
        message += f"""{item.order_item}: ${item.item_price}
        """
        if item.extras != "":
            message += f"""({item.extras})
            """
        message += """
        """
    message += f"""
    Your Total Order: ${order.total_order}

    Thanks for visiting!
    Enjoy your meal and we are waiting for you to come back!
    """

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender, "2201chacha")
    session.sendmail(sender, recipient, message)
    session.quit()

    messages.success(request, "Order has been successfully placed!")
    return HttpResponseRedirect(reverse("index"))


def show_order_view(request):
    orders = Orders.objects.all().filter(status="Has been completed")
    order = Orders.objects.get(user=request.user, status="Initiated")
    cart = All_Orders.objects.filter(user=request.user, order_id=order.pk)
    context = {
        "orders": orders,
        "cart": cart
    }

    count = 0

    for item in cart:
        count += 1
    context["count"] = count
    return render(request, "orders/orders.html", context)
