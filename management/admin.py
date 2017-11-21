from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'author','publish_date','category','description',)
    search_fields = ('name', 'price', 'author','publish_date','category',)
    list_filter = ('price','author')
    #ordering = ('-price',)
    #exclude = ('publication_date',)
    '''
    fieldsets = (
        (None, {
            'fields': ('title', 'price')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('authors', 'publisher'),
        }),
    )
    '''
class ImgAdmin(admin.ModelAdmin):
    list_display = ('name','description','img',)

'''
class FAAdmin(admin.ModelAdmin):
    name = models.CharField('Part_number',max_length=128)
    price = models.CharField('Location',max_length=128)
    author = models.CharField('Product_Line',max_length=128)
    publish_date = models.DateField('Record Date')
    category = models.CharField('Category',max_length=128)
    description = models.CharField('Description',max_length=256)
'''

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Img, ImgAdmin)
admin.site.register(FA)
