from rest_framework import serializers
from .models import Update
from .models import ProgramLaunch

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ['version', 'release_date', 'download_page', 'is_active']

class ProgramLaunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLaunch
        fields = '__all__'
        extra_kwargs = {
            'install_id': {'required': True},
            'app_name': {'required': True},
            'app_version': {'required': True}
        }