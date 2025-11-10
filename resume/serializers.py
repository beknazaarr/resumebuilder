from rest_framework import serializers
from .models import Resume
from personalinfo.models import PersonalInfo
from education.models import Education
from workexperlence.models import WorkExperience
from skill.models import Skill
from achievement.models import Achievement
from language.models import Language


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ('id', 'full_name', 'phone', 'email', 'address', 'linkedin', 'website', 'summary')
        read_only_fields = ('id',)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description', 'order')
        read_only_fields = ('id',)


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('id', 'company', 'position', 'start_date', 'end_date', 'is_current', 'description', 'order')
        read_only_fields = ('id',)

    def validate(self, data):
        if not data.get('is_current') and not data.get('end_date'):
            raise serializers.ValidationError({
                'end_date': 'Укажите дату окончания или отметьте как текущее место работы'
            })
        return data


class SkillSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Skill
        fields = ('id', 'name', 'level', 'level_display', 'category', 'category_display', 'order')
        read_only_fields = ('id',)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description', 'date', 'order')
        read_only_fields = ('id',)


class LanguageSerializer(serializers.ModelSerializer):
    proficiency_display = serializers.CharField(source='get_proficiency_level_display', read_only=True)
    
    class Meta:
        model = Language
        fields = ('id', 'language', 'proficiency_level', 'proficiency_display', 'order')
        read_only_fields = ('id',)


class ResumeListSerializer(serializers.ModelSerializer):
    """Краткий список резюме"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    personal_info_name = serializers.CharField(source='personal_info.full_name', read_only=True)
    
    class Meta:
        model = Resume
        fields = ('id', 'title', 'template', 'template_name', 'personal_info_name', 
                  'photo', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ResumeDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о резюме со всеми связанными данными"""
    personal_info = PersonalInfoSerializer(read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    work_experience = WorkExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = Resume
        fields = ('id', 'title', 'template', 'template_name', 'photo', 'is_primary',
                  'personal_info', 'education', 'work_experience', 'skills', 
                  'achievements', 'languages', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ResumeCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление резюме"""
    
    class Meta:
        model = Resume
        fields = ('title', 'template', 'photo', 'is_primary')

    def validate_is_primary(self, value):
        if value:
            user = self.context['request'].user
            # Если устанавливаем резюме как основное, снимаем флаг с других
            if self.instance:
                Resume.objects.filter(user=user, is_primary=True).exclude(pk=self.instance.pk).update(is_primary=False)
            else:
                Resume.objects.filter(user=user, is_primary=True).update(is_primary=False)
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)