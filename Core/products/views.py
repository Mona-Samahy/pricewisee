# views.py

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from .models import Brand, Product
from .serializers import  ProductSerializer
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    #serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',  'brand', 'price', 'description','url','image_url']
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64
import requests

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Convert image to base64
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Prepare data for AI model API
        payload = {
            'image_data': img_str,
            'top_n': 5  # You can adjust this based on your requirement
        }

        # Call the AI model API
        ai_model_api_url = 'https://finalfinal-1.onrender.com/predict'  # Update with your AI model API URL
        response = requests.post(ai_model_api_url, json=payload)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to get response from AI model API'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
