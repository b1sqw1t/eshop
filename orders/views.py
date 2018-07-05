from .forms                         import OrderCreateForm
from .models                        import OrderItem
from cart.cart                      import Cart
from django.urls                    import reverse_lazy
from django.contrib                 import messages
from django.shortcuts               import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid() and cart.get_total_price() > 0:
            order = form.save(commit=False)
            order.order_user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',{'order': order})
        else:
            if cart.get_total_price() == 0:
                messages.warning(request,'Не удалось оформить заказ. Корзина пуста.')
    else:
        if cart.get_total_price() <= 0:
            return redirect(reverse_lazy('index:home_page'))
        form = OrderCreateForm(initial={'first_name':request.user.first_name,
                                        'last_name':request.user.last_name,
                                        'email':request.user.email,
                                        'address':request.user.profile.Adress1,
                                        'postal_code':request.user.profile.Zip_code,
                                        'city':request.user.profile.City})
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
