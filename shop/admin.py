from django.contrib import admin
from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Admin View for Book'''

    list_display = ('title', 'num_pages',
                    'publisher', 'year', 'price')
    list_filter = ('author', 'publisher', 'price', 'year')
    list_editable = ('price',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author', 'publisher')
    date_hierarchy = 'year'
    ordering = ('-created',)
    view_on_site = True
    fieldsets = (
        ("Basic Information", {
            "fields": (('title', 'author'), 'description'),
        }),
        ("Price Information", {
            'classes': ('collapse',),
            "fields": ("price", 'discount_price')
        }),
        ("Files", {
            'classes': ('collapse',),
            "fields": ("image", "image_url", "book_file", "book_url")
        }),
        ("Meta Data", {
            'classes': ('collapse',),
            "fields": (('category', "tags"),"year", "num_pages", ("publisher", "isbn"),
                       "file_format", "slug")
        }),
        ("Featured", {
            'classes': ('collapse',),
            "fields": ("featured",)
        })
    )
