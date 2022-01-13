from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from productsapp.models import Product, ProductCategory
from authapp.models import ShopUser

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy


class UsersListView(ListView):
    model = ShopUser
    queryset = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    template_name = 'adminapp/users.html'
    extra_context = {'title': 'админка/пользователи'}
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', content)


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    extra_context = {'title': 'пользователи/создание'}
    success_url = reverse_lazy('admin_staff:users')

    # fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    extra_context = {'title': 'пользователи/редактирование'}

    # success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'

    # если нужно достать pk и передать его в success_url
    def get_success_url(self):
        print(self.object.pk)
        return reverse_lazy('admin_staff:user_update', kwargs={'pk': self.object.pk})

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')
    extra_context = {'title': 'пользователи/удаление'}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete() могли бы сделать
#         # НО вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     content = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', content)


class ProductCategoryListView(ListView):
    model = ProductCategory
    # queryset = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context_object_name = 'objects'
    template_name = 'adminapp/categories.html'
    extra_context = {'title': 'админка/категории'}

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    # fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    # fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#             # return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')
    extra_context = {'title': 'категории/удаление'}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     content = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'adminapp/category_delete.html', content)


class ProductsListView(ListView):
    # model = Product
    context_object_name = 'objects'
    template_name = 'adminapp/products.html'
    # если список пуст, то будет 404. можно обойтись без get_object_or_404
    allow_empty = False
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        # return Product.objects.filter(category=self.category).order_by('name') или так
        return Product.objects.filter(category__id=self.kwargs['pk']).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты'
        context['category'] = self.category
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукты'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     content = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', content)


# пока не нашел как жестко передать category.id в форму
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    # fields = '__all__'
    # template_name = 'adminapp/products_t.html'
    template_name = 'adminapp/product_update.html'
    extra_context = {'title': 'продукт/создание'}

    # success_url = reverse_lazy('admin_staff:products')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = self.model.category.field
    #     print(self.model.category)
    #     return context

    # def form_valid(self, form):
    #     form.instance.category__id = self.kwargs['pk']
    #     print('1111')
    #     return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # self.category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        # self.form_class = ProductEditForm(initial={'category.pk': self.category})
        # print(self.category)
        return super().dispatch(*args, **kwargs)

    # если нужно достать pk и передать его в success_url
    def get_success_url(self):
        print(self.object.pk)
        return reverse_lazy('admin_staff:products', kwargs={'pk': self.object.pk})


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'form': product_form,
        'category': category
    }

    return render(request, 'adminapp/product_update.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/подробнее'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product, }
#
#     return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'form': edit_form,
        'category': edit_product.category
    }

    return render(request, 'adminapp/product_update.html', content)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin_staff:categories')
    extra_context = {'title': 'продукт/удаление'}
    context_object_name = 'product_to_delete'
    # allow_empty = False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', kwargs={'pk': self.object.category.pk})


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))
#
#     content = {'title': title, 'product_to_delete': product}
#
#     return render(request, 'adminapp/product_delete.html', content)
