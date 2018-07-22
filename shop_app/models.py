from django.db import models

# Создаем базовую модель нашего продукта
class Product(models.Model): 
    title = models.CharField(max_length=200) # и указываем максимальную длину
    description = models.TextField(max_length=5000)
    category = models.ForeignKey('Category', on_delete='CASCADE', null=True, related_name="products") 

    def __str__(self):
        return self.title

class Category(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return self.title