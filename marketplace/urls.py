from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Landing page for guests, product list for logged-in users
    path('', views.LandingView.as_view(), name='landing'),
    path('listings/', views.ProductListView.as_view(), name='product_list'),

    # My listings dashboard
    path('my-listings/', views.MyListingsView.as_view(), name='my_listings'),

    # Product CRUD
    path('listings/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('listings/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('listings/<int:pk>/edit/', views.ProductEditView.as_view(), name='product_edit'),
    path('listings/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Actions
    path('listings/<int:pk>/sold/', views.mark_as_sold, name='mark_as_sold'),
    path('images/<int:image_id>/delete/', views.delete_product_image, name='delete_image'),
]