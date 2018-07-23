# импортируем модель для CBV            
from django.views import generic 

# импортируем нашу модель
from .models import Product,Category

class MainView(generic.ListView):
    
    template_name = 'main.html' # подключаем наш Темплейт
    context_object_name = 'categories'# под каким именем передадутся данные в Темплейт
    model = Category # название Модели
    
    # метод для добавления дополнительной информации в контекст
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # передаем в словарь контекста список всех продуктов 
        context['products'] = Product.objects.all()
        return context

class CategoryDetail(generic.DetailView): 
    template_name = 'category_detail.html' 
    model = Category
    
    # def get_context_data(self, **kwargs): 
    #     context = super().get_context_data(**kwargs)

    #     #Благодаря foreignkey в модели Product из экземпляра категории можно получить все товары, через обратный вызов 
    #     context['products'] = Category.products.all()
    #     return context

class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product