from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.http import Http404
from django.db.models import Q, Count

from .models import Product, ProductImage, Category
from .forms import ProductForm


# ─────────────────────────────────────────────
# Landing Page (logged-out users)
# ─────────────────────────────────────────────

class LandingView(View):
    """
    Shows a marketing landing page to logged-out visitors.
    Logged-in users are sent straight to the product listing.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('marketplace:product_list')

        # Grab a few recent products to show as preview
        recent_products = Product.objects.filter(
            is_active=True, is_sold=False
        ).prefetch_related('images').order_by('-created_at')[:6]

        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(
                products__is_active=True,
                products__is_sold=False
            ))
        )

        return render(request, 'landing.html', {
            'recent_products': recent_products,
            'categories': categories,
        })


# ─────────────────────────────────────────────
# Product List View (Homepage)
# ─────────────────────────────────────────────

class ProductListView(View):
    """
    Displays all active, unsold product listings.
    Supports search by keyword and filter by category.
    """
    template_name = 'marketplace/product_list.html'

    def get(self, request):
        products = Product.objects.filter(
            is_active=True, is_sold=False
        ).select_related('seller', 'category').prefetch_related('images')

        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(
                products__is_active=True,
                products__is_sold=False
            ))
        )

        query = request.GET.get('q', '').strip()
        if query:
            products = products.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        category_slug = request.GET.get('category', '').strip()
        active_category = None
        if category_slug:
            active_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=active_category)

        condition = request.GET.get('condition', '').strip()
        if condition:
            products = products.filter(condition=condition)

        sort = request.GET.get('sort', 'newest')
        if sort == 'price_low':
            products = products.order_by('price')
        elif sort == 'price_high':
            products = products.order_by('-price')
        else:
            products = products.order_by('-created_at')

        context = {
            'products': products,
            'categories': categories,
            'query': query,
            'active_category': active_category,
            'condition': condition,
            'sort': sort,
            'total_count': products.count(),
            'condition_choices': Product.CONDITION_CHOICES,
        }
        return render(request, self.template_name, context)



# ─────────────────────────────────────────────
# Product Detail View
# ─────────────────────────────────────────────

class ProductDetailView(View):
    template_name = 'marketplace/product_detail.html'

    def get(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('seller', 'category').prefetch_related('images'),
            pk=pk,
            is_active=True
        )
        # Fetch 4 related listings from same category, exclude current
        related_products = Product.objects.filter(
            is_active=True,
            is_sold=False,
            category=product.category
        ).exclude(pk=pk).prefetch_related('images')[:4]

        context = {
            'product': product,
            'is_seller': request.user == product.seller,
            'related_products': related_products,
        }
        return render(request, self.template_name, context)

# ─────────────────────────────────────────────
# Product Create View
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class ProductCreateView(View):
    template_name = 'marketplace/product_form.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {
            'form': form,
            'page_title': 'Post a New Listing'
        })

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            # ✅ FIX: Read images from cleaned_data, not FILES.getlist()
            # Our custom MultipleFileField returns a list in cleaned_data
            images = form.cleaned_data.get('images')
            if images:
                # Handle both single file and list of files
                if not isinstance(images, list):
                    images = [images]
                for image_file in images:
                    ProductImage.objects.create(product=product, image=image_file)

            messages.success(request, "Your listing has been posted! 🎉")
            return redirect('marketplace:product_detail', pk=product.pk)

        return render(request, self.template_name, {
            'form': form,
            'page_title': 'Post a New Listing'
        })


# ─────────────────────────────────────────────
# Product Edit View (Seller Only)
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class ProductEditView(View):
    template_name = 'marketplace/product_form.html'

    def get_product(self, pk, user):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        if product.seller != user:
            raise Http404("You are not authorized to edit this listing.")
        return product

    def get(self, request, pk):
        product = self.get_product(pk, request.user)
        form = ProductForm(instance=product)
        return render(request, self.template_name, {
            'form': form,
            'product': product,
            'page_title': 'Edit Listing',
            'existing_images': product.images.all(),
        })

    def post(self, request, pk):
        product = self.get_product(pk, request.user)
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            # ✅ FIX: Read images from cleaned_data, not FILES.getlist()
            images = form.cleaned_data.get('images')
            if images:
                if not isinstance(images, list):
                    images = [images]
                for image_file in images:
                    ProductImage.objects.create(product=product, image=image_file)

            messages.success(request, "Listing updated successfully!")
            return redirect('marketplace:product_detail', pk=product.pk)

        return render(request, self.template_name, {
            'form': form,
            'product': product,
            'page_title': 'Edit Listing',
            'existing_images': product.images.all(),
        })
    
# ─────────────────────────────────────────────
# Product Delete View (Seller Only)
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(View):
    """
    Allows only the seller to delete their own listing.
    Shows a confirmation page before deleting.
    """
    template_name = 'marketplace/product_confirm_delete.html'

    def get_product(self, pk, user):
        product = get_object_or_404(Product, pk=pk)
        if product.seller != user:
            raise Http404("You are not authorized to delete this listing.")
        return product

    def get(self, request, pk):
        product = self.get_product(pk, request.user)
        return render(request, self.template_name, {'product': product})

    def post(self, request, pk):
        product = self.get_product(pk, request.user)
        product.delete()
        messages.success(request, "Your listing has been deleted.")
        return redirect('marketplace:product_list')


# ─────────────────────────────────────────────
# Mark as Sold (Seller Only)
# ─────────────────────────────────────────────

@login_required
def mark_as_sold(request, pk):
    """
    Toggles the sold status of a product.
    Only the seller can mark/unmark their product as sold.
    """
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        messages.error(request, "You can only update your own listings.")
        return redirect('marketplace:product_detail', pk=pk)

    if request.method == 'POST':
        # Toggle sold status
        product.is_sold = not product.is_sold
        product.save()

        status = "sold" if product.is_sold else "available again"
        messages.success(request, f'"{product.title}" marked as {status}.')

    return redirect('marketplace:product_detail', pk=pk)


# ─────────────────────────────────────────────
# Delete Single Product Image (Seller Only)
# ─────────────────────────────────────────────

@login_required
def delete_product_image(request, image_id):
    """
    Standalone view to delete a single image.
    ✅ FIX: This is now a completely separate endpoint,
    not a nested form — avoids the parent form submission bug.
    """
    image = get_object_or_404(ProductImage, pk=image_id)

    if image.product.seller != request.user:
        messages.error(request, "You cannot delete this image.")
        return redirect('marketplace:product_detail', pk=image.product.pk)

    if request.method == 'POST':
        product_pk = image.product.pk
        image.delete()
        messages.success(request, "Image removed.")
        return redirect('marketplace:product_edit', pk=product_pk)

    return redirect('marketplace:product_detail', pk=image.product.pk)

# ─────────────────────────────────────────────
# My Listings (Seller Dashboard)
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class MyListingsView(View):
    """
    Shows all listings posted by the currently logged-in user.
    Includes active, sold, and inactive listings.
    """
    template_name = 'marketplace/my_listings.html'

    def get(self, request):
        all_listings = Product.objects.filter(
            seller=request.user
        ).prefetch_related('images').order_by('-created_at')

        # Separate by status for tabs
        active_listings = all_listings.filter(is_active=True, is_sold=False)
        sold_listings = all_listings.filter(is_sold=True)

        context = {
            'all_listings': all_listings,
            'active_listings': active_listings,
            'sold_listings': sold_listings,
            'active_count': active_listings.count(),
            'sold_count': sold_listings.count(),
            'total_count': all_listings.count(),
        }
        return render(request, self.template_name, context)