from rest_framework import serializers
from .models import PersonalInfo


class PersonalInfoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ('full_name', 'phone', 'email', 'address', 'linkedin', 'website', 'summary')

    def validate_email(self, value):
        if value and '@' not in value:
            raise serializers.ValidationError("Введите корректный email адрес")
        return value

    def validate_full_name(self, value):
        if not value or len(value) < 2:
            raise serializers.ValidationError("ФИО должно содержать минимум 2 символа")
        return value