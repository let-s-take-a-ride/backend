from rest_framework import serializers
from .models import CustomUser, UserPreferences


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['distance', 'average', 'city']


class CustomUserSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer()
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'first_login', 'preferences', 'picture']

    # class Meta:
    #     model = CustomUser
    #     fields = '__all__'

    def update(self, instance, validated_data):
        preferences_data = validated_data.pop('preferences', None)
        super().update(instance, validated_data)

        if preferences_data:
            preferences, created = UserPreferences.objects.get_or_create(user=instance)
            for attr, value in preferences_data.items():
                setattr(preferences, attr, value)
            preferences.save()

        return instance
