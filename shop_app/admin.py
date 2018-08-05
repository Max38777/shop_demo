from django.contrib import admin

# импортируем нашу модель
from .models import Product,Category,Order

# говорим админке зарегистрировать нашу модель
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)