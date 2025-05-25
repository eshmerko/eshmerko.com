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
        fields = ['install_id', 'app_name', 'app_version', 'system_platform', 'python_version']
        extra_kwargs = {
            'install_id': {'validators': []},  # Disable uniqueness validator
            'system_platform': {'required': False, 'allow_blank': True},
            'python_version': {'required': False, 'allow_blank': True},
        }

    def validate_install_id(self, value):
        """Ensure install_id is a valid UUID."""
        import uuid
        try:
            uuid.UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format.")
        return value