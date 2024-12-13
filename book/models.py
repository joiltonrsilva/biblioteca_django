from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=60,
    )
    description = models.TextField(
        verbose_name=_('Description'),
    )
    author = models.CharField(
        verbose_name=_('Author'),
        max_length=40,
    )
    category = models.ForeignKey(
        to='book.Category',
        verbose_name=_('Category'),
        on_delete=models.RESTRICT,
        related_name='book_category_category',
    )
    quantity_registred = models.IntegerField(
        verbose_name=_('Quantity Registred'),
    )
    loan_quantity = models.IntegerField(
        verbose_name=_('Loan Quantity'),
        default=0,
    )
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True,
    )
    last_modified = models.DateTimeField(
        verbose_name=_('Last Modified'),
        auto_now=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=40,
    )
    description = models.TextField(
        verbose_name=_('Description')
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name
    

class ImageBook(models.Model):
    path = models.ImageField(
        verbose_name=_('Image'),
        upload_to='book',
    )
    book: models.ForeignKey(
        to='book.Book',
        verbose_name=_('Book'),
        on_delete=models.RESTRICT,
        related_name='imagebook_book_book',
    )
