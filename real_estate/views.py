from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class AllProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Only authenticated users can access this viewset

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(user=user)
        return Product.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        user_plan = user.plan
        user_product_count = Product.objects.filter(user=user).count()

        if user_product_count >= user_plan.number_of_post:
            raise ValidationError(f"Post limit exceeded. Your plan allows for {user_plan.number_of_post} posts.")

        serializer.save(user=user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            profile_photo_url = None
            user_plan = user.plan
            plan_serializer = PlanSerializer(user_plan)
            if user.profile_photo:
                profile_photo_url = request.build_absolute_uri(user.profile_photo.url)

            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'profile_photo_url': profile_photo_url,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'plan': plan_serializer.data,
                'role': user.role
            })
        else:
            return JsonResponse({'error': 'Incorrect username or password.'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        profile_photo = data.get('profile_photo')
        email = data.get('email')
        plan_name = data.get('plan')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        # Get the plan instance or the default 'Free' plan if none is provided
        if plan_name:
            plan = get_object_or_404(Plan, name=plan_name)
        else:
            plan = get_object_or_404(Plan, name='Free')

        # Create the user with the plan instance
        user = CustomUser.objects.create_user(username=username, password=password,
                                              profile_photo=profile_photo, email=email, plan=plan)

        user.save()

        return JsonResponse({'message': 'User created successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'User logged out successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
