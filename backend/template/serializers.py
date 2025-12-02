from rest_framework import serializers
from .models import Template


class TemplateListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка шаблонов"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Template
        fields = ('id', 'name', 'description', 'preview_image', 'is_active', 
                  'created_by_username', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TemplateDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор шаблона с HTML/CSS"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Template
        fields = ('id', 'name', 'description', 'preview_image', 'html_structure', 
                  'css_styles', 'is_active', 'created_by', 'created_by_username',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')


class TemplateCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления шаблона (для админов)"""
    
    class Meta:
        model = Template
        fields = ('name', 'description', 'preview_image', 'html_structure', 
                  'css_styles', 'is_active')

    def validate_name(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError("Название должно содержать минимум 3 символа")
        return value

    def validate_html_structure(self, value):
        if not value:
            raise serializers.ValidationError("HTML структура обязательна")
        return value

    def validate_css_styles(self, value):
        if not value:
            raise serializers.ValidationError("CSS стили обязательны")
        return value