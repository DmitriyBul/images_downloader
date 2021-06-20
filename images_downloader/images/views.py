from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# Create your views here.
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from images.models import Picture
from images.serializers import PictureSerializer


class PictureViewSet(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        max_size = 200000
        file_serializer = PictureSerializer(data=request.data)
        if file_serializer.is_valid():
            if request.FILES['image'].size > max_size:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # queryset = Picture.objects.all()
    # serializer_class = PictureSerializer
    # permission_classes = [IsAuthenticated]


@login_required
def upload(request):
    context = {}
    max_size = 200000
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        existing_image = Picture.objects.filter(name=uploaded_file.name)
        if existing_image:
            messages.warning(request, 'Данное название изображения недоступно')
        if request.FILES['document'].size > max_size:
            messages.warning(request, 'Файл весит больше 200 Кб')
        else:
            name = fs.save(uploaded_file.name, uploaded_file)
            downloaded_image = Picture.objects.get_or_create(name=uploaded_file.name, image=uploaded_file)
            # downloaded_image.save()
            # context['url'] = fs.url(name)
    return render(request, 'upload.html')
