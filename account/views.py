from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from account.forms    import EmailPostForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.urls      import reverse_lazy
from account.models   import Profile
from orders.models    import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

def test(request):
    return render(request,'my_account.html')

@login_required
def my_account(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request,'registration/profile.html',{'user_profile':user_profile})


def post_share(request):
    # Отправка почты...ТЕСТ
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = 'Radio_fm.ru. Отправитель {} ({})  "{}"'.format(cd['name'], cd['email'], cd['title'])
            message = '{}'.format(cd['comments'])
            send_mail(subject, message, 'bisqwit@yandex.ru',[cd['to']])
            sent = True
            return redirect(reverse_lazy('account:post_share'))
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'form': form,
                                                    'sent': sent})

def register(request):
    #Регистрация пользователя
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = new_user,
            profile = Profile.objects.create(user=new_user,
                                             Company=profile_form.cleaned_data['Company'],
                                             Telephone=profile_form.cleaned_data['Telephone'],
                                             Fax=profile_form.cleaned_data['Fax'],
                                             Adress1=profile_form.cleaned_data['Adress1'],
                                             Adress2=profile_form.cleaned_data['Adress2'],
                                             City=profile_form.cleaned_data['City'],
                                             State=profile_form.cleaned_data['State'],
                                             Country=profile_form.cleaned_data['Country'],
                                             Zip_code=profile_form.cleaned_data['Zip_code'])
            profile.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'registration/register.html', {'user_form': user_form,
                                                          'profile_form':profile_form})


from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

@login_required
def edit(request):
    #Изменение данных пользователя через личный кабинет
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,files=request.FILES)
        if user_form.is_valid() or profile_form.is_valid():
            if user_form.is_valid():
                form = user_form.save(commit=False)
                form.user = request.user
                form.save()
            else:
                user_form = UserEditForm(instance=request.user)
                profile_form = ProfileEditForm(instance=request.user.profile)
                return render(request,
                              'registration/edit_profile.html',
                              {'user_form': user_form,
                               'profile_form': profile_form})
            if profile_form.is_valid():
                print('VALIDыуцц')
                profile_form.save()
            else:
                user_form = UserEditForm(instance=request.user)
                profile_form = ProfileEditForm(instance=request.user.profile)
                return render(request,
                              'registration/edit_profile.html',
                              {'user_form': user_form,
                               'profile_form': profile_form})
            return redirect(reverse_lazy('account:my_account'))
        else:
            return render(request,
                          'registration/edit_profile.html',
                          {'user_form': user_form,
                           'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'registration/edit_profile.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


def view_profile(request,id):
    object = get_object_or_404(User, id=id)
    return render(request,'registration/view_profile.html',{'object':object})


@login_required
def view_history(request):
    object = Order.objects.filter(order_user=request.user).prefetch_related('items')
    return render(request,'registration/view_history.html',{'object':object})



class Reg(FormView):
    form_class = ProfileEditForm
    success_url = '/'
    template_name = 'registration/reg.html'

    def get_initial(self):
        user = User.objects.get(id=1)
        object = Profile.objects.get(user=user)
        return super(Reg,self).get_initial()
    def form_valid(self, form):

        form.save()
        return super(Reg,self).form_valid(form)

    def form_invalid(self, form):
        return super(Reg,self).form_invalid(form)