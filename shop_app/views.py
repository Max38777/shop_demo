# импортируем модель для CBV            
from django.views import generic 
# импортируем нашу модель
from .models import Product,Category,Order
from django.conf.urls import include
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

class ProductCreate(generic.CreateView): 
	model = Product 
	# название нашего шаблона с формой
	template_name = 'product_new.html' 
	# какие поля будут в форме 
	fields = '__all__'

class OrderFormView(LoginRequiredMixin, generic.CreateView): 
    model = Order 
    template_name = 'order_form.html' 
    success_url = '/' 
    #fields = '__all__'
    fields = ['customer_name', 'customer_phone']
  
    def get_initial(self):
        first_name = self.request.user.first_name
        return {'customer_name': first_name}

    def form_valid(self, form):
        # получаем ID из ссылки и передаем в ORM для фильтрации
        product = Product.objects.get(id=self.kwargs['pk']) 
        # передаем в поле товара нашей формы отфильтрованный товар
        form.instance.product = product 
        # получаем пользователя из сессии
        user = self.request.user
        # передаем в поле формы
        form.instance.user = user
        # super — перезагружает форму, нужен для работы
        return super().form_valid(form)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['pk'])
        context['product'] = product
        context['user'] = self.request.user
        return context

class SignUpView(generic.CreateView): 
    form_class = UserCreationForm 
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'