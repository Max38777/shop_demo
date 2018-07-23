from django.contrib import admin

# импортируем нашу модель
from .models import Product
from .models import Category

# говорим админке зарегистрировать нашу модель
admin.site.register(Product)
admin.site.register(Category)