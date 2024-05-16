# views.py

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand__name', 'brand__id', 'price', 'description','url']
    from django.shortcuts import render

    # Create your views here.

    # views.py
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from .models import Product
    from .serializers import ProductSerializer

    class PriceComparisonAPIView(APIView):
        def get(self, request, price_to_compare, format=None):
            products = Product.objects.filter(price__lte=price_to_compare)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

