from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from . import views



# Define your viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'allproducts', AllProductViewSet, basename='Allproducts')
router.register(r'plans', PlanViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'contact', ContactViewSet)

# Add your custom URL patterns
urlpatterns = [
    # URL patterns generated by router
    *router.urls,
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    # path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    # path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),
]
