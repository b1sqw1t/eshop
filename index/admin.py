from django.contrib import admin
from index.models import *



class Product_brand_Admin(admin.ModelAdmin):
    list_display = ['brand_name','brand_country']
admin.site.register(Product_brand,Product_brand_Admin)

class Product_category_Admin(admin.ModelAdmin):
    list_display = ['category_name',]
admin.site.register(Product_category,Product_category_Admin)

class Product_picture_Admin(admin.ModelAdmin):
    list_display = ['product',]
admin.site.register(Product_picture,Product_picture_Admin)

class Product_picture_inline(admin.TabularInline):
    model = Product_picture
    extra = 1

class Product_Admin(admin.ModelAdmin):
    list_display = ['product_name','product_brand','product_category','product_visible','slug']
    inlines = [Product_picture_inline]
    search_fields = ['product_name',]
    list_filter = ['product_brand','product_category','product_visible']
admin.site.register(Product,Product_Admin)
