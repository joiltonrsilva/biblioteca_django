from typing import Any

from django.contrib import admin
from django.db.models import QuerySet
from django import forms

from .models import Book, Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]
    
    def clean(self) -> Any:
        cleaned_data = super().clean()
        instance = self.instance

        if cleaned_data is not None:
            name: str = cleaned_data.get('name')

            if not instance:
                category: QuerySet = Category.objects.filter(
                    name=name
                ).exists()
            
                if category:
                    self.add_error(None, 'Categoria já existe')
            else:
                category: QuerySet = Category.objects.exclude(
                    id=instance.id
                ).filter(name=name).exists()

                if category:
                    self.add_error(None, 'Categoria já existe')

        return cleaned_data


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm

    list_display = (
        'id',
        'name',
        'description',
    )

    list_filter = (
        'name',
    )
    search_fields = (
        'name__istartswitch',
    )


class BookForm(forms.Form):

    class Meta:
        model = Book
        fiels = [
            'name',
            'description',
            'author',
            'category',
            'quantity_registred',
        ]

    def clean(self) -> Any:

        cleaned_data = self.clean()
        instance = self.instance
        if cleaned_data is not None:
            name = cleaned_data.get('name')
            author = cleaned_data.get('author')
            category = cleaned_data.get('category')
            quantity_registred = cleaned_data.get('quantity_registred')

            if not instance:
                books: QuerySet = Book.objects.filter(
                    name=name,
                    author=author,
                    category=category
                ).exists()
                if books:
                    return self.add_error(None, 'Livro já existe')
            else:
                books: QuerySet = Book.objects.exclude(id=instance.id).filter(
                    name=name,
                    author=author,
                    category=category
                ).exists()
                if books:
                    return self.add_error(None, 'Livro já existe')
                
                if quantity_registred < instance.quantity_registred:
                    return self.add_error(
                        None,
                        'A quantidade não pode ser menor a quantidade emprestada'
                    )

        return cleaned_data
