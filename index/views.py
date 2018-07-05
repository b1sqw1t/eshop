from index.forms                    import search_form
from index.models                   import Product,Product_brand,Product_category
from cart.forms                     import CartAddProductForm
from comments.forms                 import comments_form
from comments.models                import Comment
from django.shortcuts               import render,redirect
from django.views.generic.base      import TemplateView
from django.views.generic.list      import ListView
from django.views.generic.detail    import DetailView
from django.views.generic           import FormView
from django.http                    import HttpResponse,Http404
from django.db.models               import Q

def test(request):
    from datetime import datetime
    time = datetime.now()
    if request.POST:
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        print(user_name)
    return render(request,'index/test.html',{'time':time})

def check(request):
    if request.GET:
        user_name = request.GET.get('user_name')
        print(user_name)
        return HttpResponse('ok',content_type='text/html')
    else:
        return HttpResponse('no',content_type='text/html')



class home_page(TemplateView):
    template_name = 'index/index.html'


    def get(self,request,*args,**kwargs):

        self.new_product = Product.objects.order_by('-product_created').\
                                           filter(product_new=True,product_visible=True,product_count__gt=0). \
                                           defer('product_category','product_description','product_visible','product_count','product_views','product_created','product_changed').\
                                           prefetch_related('images')[0:6]

        self.featured = Product.objects.order_by('-product_views').\
                                                filter(product_visible=True,product_count__gt=0). \
                                                defer('product_category','product_description','product_visible','product_count','product_views','product_created','product_changed').\
                                                prefetch_related('images')

        self.last_comments = Comment.objects.order_by('-Created')[:3]
        return super(home_page,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(home_page,self).get_context_data(**kwargs)
        context['new_product'] = self.new_product
        context['featured'] = self.featured
        context['product_brand'] = Product_brand.objects.all()
        context['last_comments'] = self.last_comments
        return context

class product_view(DetailView):
    model = Product
    template_name = 'index/product.html'
    slug_field = 'product_slug'
    slug_url_kwarg = 'model'

    def get(self,request,*args,**kwargs):
        try:
            self.object = Product.objects.get(product_slug=kwargs['model'])
        except:
            raise Http404
        self.page_title = 'Купить %s %s %s' %(self.object.product_category,self.object.product_brand,self.object.product_name)
        self.cart_product_form = CartAddProductForm()
        self.comments = Comment.objects.filter(Product=self.object)
        self.comments_form = comments_form(initial={'Product':self.object,
                                                    'User':self.request.user})
        self.object.product_views += 1
        self.object.save()

        return super(product_view,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(product_view,self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['cart_product_form'] = self.cart_product_form
        context['comments'] = self.comments
        context['comments_form'] = self.comments_form
        return context

class category_view(ListView):
    model = Product
    template_name = 'index/category.html'

    def get(self, request, *args, **kwargs):
        try:#Проверка на изменение типа отображения товаров (сетка или список)
            self.request.session['view'] = request.GET['view']
        except:
            pass
        try:#Изменяет отображение количества товаров на странице
            if self.request.GET['page_in']:
                self.request.session['page_in'] = self.request.GET['page_in']
            self.paginate_by = self.request.session['page_in']
        except:
            try:
                if not self.request.session['page_in']:
                    self.paginate_by = self.request.session['page_in']= 9
                else:
                    self.paginate_by = self.request.session['page_in']
            except:
                self.paginate_by = self.request.session['page_in'] = 9
        try:#Проверяет отображать ли все товары или какую то категорию
            if kwargs['type']:
                self.obj = Product.objects.filter(product_category__category_slug=kwargs['type'])
            else:
                self.obj = Product.objects.all()
        except:
            self.obj = Product.objects.all()

        self.category_list = Product_category.objects.all()#Для отображения всех категорий товаров
        self.brand_list = Product_brand.objects.all()#Для отображения всех производителей товаров
        return super(category_view,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(category_view,self).get_context_data(**kwargs)
        context['category_list'] = self.category_list
        context['brand_list'] = self.brand_list

        return context

    def get_queryset(self):
        return self.obj

def product_like(request,model=None):
    referer = request.META['HTTP_REFERER']

    try:
        object = Product.objects.get(product_slug=model)
        object.product_like += 1
        object.product_rating = object.get_rating()
        object.save()
    except:
        pass
    return redirect(str(referer))

def product_dislike(request,model=None):
    referer = request.META['HTTP_REFERER']
    try:
        object = Product.objects.get(product_slug=model)
        object.product_dislike += 1
        object.product_rating = object.get_rating()
        object.save()
    except:
        pass
    return redirect(str(referer))


class search(FormView):
    form_class = search_form
    template_name = 'index/category.html'


    def get(self, requset,*args,**kwargs):
        return super(search,self).get(requset,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        self.search_text = request.POST.get('input_search_text',None)
        return super(search,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(search, self).get_context_data(**kwargs)
        try:
            context['object_list'] = Product.objects.filter(
                Q(product_name__icontains=self.search_text) | Q(product_brand__brand_name__icontains=self.search_text))
        except:
            context['object_list'] = None
        return context




# def search(request):
#     search = request.POST.get('input_search_text', None)
#     if search:
#         response = Product.objects.filter(
#             Q(product_name__icontains=search) | Q(product_brand__brand_name__icontains=search))
#         print(response)
#         return render(request=request,template_name='index/category.html',context={'search':search,
#                                                                                    'object_list':response})
#     return redirect('index:home_page')