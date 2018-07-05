from django.contrib import admin
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('Text','User','Product','Visible','Created','Changed')
    list_filter = ('Created','Visible')
    search_fields = ('User__username','Text','Product__product_name')
admin.site.register(Comment,CommentAdmin)


# Register your models here.
