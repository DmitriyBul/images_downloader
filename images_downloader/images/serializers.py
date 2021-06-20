from rest_framework.serializers import ModelSerializer

from images.models import Picture


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
