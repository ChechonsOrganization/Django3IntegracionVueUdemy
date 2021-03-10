from django.contrib import admin
# modelos
from .models import Element, Category, Type, ElementImages
# import-export, admin, field
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

class ElementResource(resources.ModelResource):
    #id = Field(attribute="id", column_name="#ID")
    class Meta:
        model = Element
        #fields = ('id','title','url_clean','type')
        #export_order = ('url_clean','id','title','type')
        #exclude = ('id')

    #def dehydrate_id(self, e):
    #    return '# %s' % (e.id)

# crear clase para administrar las imagenes de los productos
class ElementImagesInLine(admin.StackedInline):
    exclude = ('base_cover_name','base_cover_ext')
    model = ElementImages
    extra = 3

class ElementAdmin(ImportExportModelAdmin):
    resource_class = ElementResource
    list_display = ('id','title')
    inlines = [ElementImagesInLine]

class TypeResource(resources.ModelResource):
    class Meta:
        model = Type
        exclude = ('id')

class TypeAdmin(ImportExportModelAdmin):
    resource_class = TypeResource
    list_display = ('id','title')


# class TypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

#class ElementAdmin(admin.ModelAdmin):
#    list_display = ('id', 'title','description','category','type')

admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Element, ElementAdmin)
