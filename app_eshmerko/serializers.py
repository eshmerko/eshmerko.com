from rest_framework import serializers
from .models import Update

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ['version', 'release_date', 'download_page', 'is_active']