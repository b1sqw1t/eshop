from django.shortcuts               import render,redirect
from comments.models                import Comment
from comments.forms                 import comments_form
from django.views.decorators.http   import require_POST
from django.urls                    import reverse_lazy


@require_POST
def add_comment(request):
    form = comments_form(request.POST)
    if request.user.is_authenticated:
        if form.is_valid():
            form.save()
            return redirect(form.cleaned_data['Product'])
    return redirect(form.cleaned_data['Product'])

def del_comment(request,id):
    comment = Comment.objects.get(id=id)
    ret = comment.Product
    if comment.User == request.user:
        comment.delete()
    return redirect(ret)