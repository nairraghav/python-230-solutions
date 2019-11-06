from django.contrib import admin
from blogging.models import Post, Category


class PostAdmin(admin.ModelAdmin):
    pass


class PostInline(admin.TabularInline):
    model = Post


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        PostInline,
    ]

    exclude = ('posts',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
