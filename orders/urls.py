from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("add_item", views.add_item_view, name="add_item"),
    path("cart_item", views.cart_item_view, name="cart_item"),
    path("remove_order", views.remove_order_view, name="remove_order"),
    path("place_order", views.place_order_view, name="place_order"),
    path("show_order", views.show_order_view, name="show_order"),
]
