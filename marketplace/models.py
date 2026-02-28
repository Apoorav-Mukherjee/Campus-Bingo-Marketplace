from django.db import models
from django.conf import settings
from django.urls import reverse
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True,
                            help_text="Bootstrap icon class e.g. bi-book")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('marketplace:product_list') + f'?category={self.slug}'


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products'
    )

    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Helps Pylance resolve the reverse relation from ProductImage
    if TYPE_CHECKING:
        images: RelatedManager['ProductImage']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.seller.username}"

    def get_absolute_url(self):
        return reverse('marketplace:product_detail', kwargs={'pk': self.pk})

    def get_primary_image(self):
        """Returns the first uploaded image or None."""
        return self.images.first()

    @property
    def is_available(self):
        return self.is_active and not self.is_sold


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.product.title}"