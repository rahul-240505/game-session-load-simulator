from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        This method correctly hashes the password.
        """
        user = User.objects.create_user(**validated_data)
        return user
