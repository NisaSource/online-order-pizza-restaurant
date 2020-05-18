from django.contrib import admin
from .models import Menu_Pizza, Menu_Topping, Menu_Sub, Menu_Pasta, Menu_Salad, Menu_Dinner_Platter, Menu_Extra, Orders, All_Orders

admin.site.register(Menu_Pizza)
admin.site.register(Menu_Topping)
admin.site.register(Menu_Sub)
admin.site.register(Menu_Pasta)
admin.site.register(Menu_Salad)
admin.site.register(Menu_Dinner_Platter)
admin.site.register(Menu_Extra)
admin.site.register(Orders)
admin.site.register(All_Orders)
