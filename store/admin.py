from django.contrib import admin

from .models import Category, Product, Department, TeamMember, Testimonial,Banner,ProductSpecification, ProductFeature, ProductSupport

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Department)
admin.site.register(TeamMember)
admin.site.register(Testimonial)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'created_at')
    list_editable = ('order', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'subtitle')

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value']
    list_filter = ['product']
    search_fields = ['name', 'value', 'product__name']

@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'is_highlighted']
    list_filter = ['product', 'is_highlighted']
    search_fields = ['title', 'description', 'product__name']

@admin.register(ProductSupport)
class ProductSupportAdmin(admin.ModelAdmin):
    list_display = ['product', 'doc_type', 'title']
    list_filter = ['product', 'doc_type']
    search_fields = ['title', 'product__name']