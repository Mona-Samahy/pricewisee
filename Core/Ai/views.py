'''
#from django.http import jasonresponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Core.Ai.mymodel.modelfinal import feature_list, filenames ,model ,neighbors
from mymodel import modelfinal
import mymodel as find_similar_images
#from .utils.model_utils import find_similar_images


@csrf_exempt
def find_similar_images_api(request):
    if request.method == 'POST':
        # استخراج معرّف الصورة من الطلب المرسل عبر Insomnia
        try:
            photo_id = int(request.POST.get('photo_id'))
        except ValueError:
            return JsonResponse({'error': 'Invalid photo_id'}, status=400)

        # استخدام النموذج للعثور على الصور المماثلة
        similar_images = find_similar_images(photo_id, feature_list, filenames, model, neighbors)

        # إعادة الاستجابة بقائمة الصور المماثلة
        return JsonResponse({'similar_images': similar_images})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
  '''
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class ModelAPIView(APIView):
    def get(self, request):
        url = "https://pricewice-ht8a.onrender.com/"
        response = requests.get(url)
        data = response.json()
        return Response(data)
