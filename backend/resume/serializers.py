from rest_framework import serializers
from .models import Resume
from personalinfo.models import PersonalInfo
from education.models import Education
from workexperlence.models import WorkExperience
from skill.models import Skill
from achievement.models import Achievement
from language.models import Language


class PersonalInfoSerializer(serializers.ModelSerializer):
    """Сериализатор личной информации"""
    class Meta:
        model = PersonalInfo
        fields = ('id', 'full_name', 'phone', 'email', 'address', 'linkedin', 'website', 'summary')
        read_only_fields = ('id',)


class EducationSerializer(serializers.ModelSerializer):
    """Сериализатор образования"""
    class Meta:
        model = Education
        fields = ('id', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description', 'order')
        read_only_fields = ('id',)
    
    def validate(self, data):
        """Проверка корректности дат"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'Дата окончания не может быть раньше даты начала'
            })
        
        return data


class WorkExperienceSerializer(serializers.ModelSerializer):
    """Сериализатор опыта работы"""
    class Meta:
        model = WorkExperience
        fields = ('id', 'company', 'position', 'start_date', 'end_date', 'is_current', 'description', 'order')
        read_only_fields = ('id',)

    def validate(self, data):
        """Валидация данных опыта работы"""
        is_current = data.get('is_current', False)
        end_date = data.get('end_date')
        start_date = data.get('start_date')
        
        # Если не текущее место работы, дата окончания обязательна
        if not is_current and not end_date:
            raise serializers.ValidationError({
                'end_date': 'Укажите дату окончания или отметьте как текущее место работы'
            })
        
        # Если текущее место работы, дата окончания должна быть пустой
        if is_current and end_date:
            raise serializers.ValidationError({
                'end_date': 'Для текущего места работы не указывается дата окончания'
            })
        
        # Проверка корректности дат
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'Дата окончания не может быть раньше даты начала'
            })
        
        return data


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор навыков"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Skill
        fields = ('id', 'name', 'level', 'level_display', 'category', 'category_display', 'order')
        read_only_fields = ('id',)


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор достижений"""
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description', 'date', 'order')
        read_only_fields = ('id',)


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор языков"""
    proficiency_display = serializers.CharField(source='get_proficiency_level_display', read_only=True)
    
    class Meta:
        model = Language
        fields = ('id', 'language', 'proficiency_level', 'proficiency_display', 'order')
        read_only_fields = ('id',)


class ResumeListSerializer(serializers.ModelSerializer):
    """Краткий список резюме для отображения в списке"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    personal_info_name = serializers.SerializerMethodField()
    has_complete_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = ('id', 'title', 'template', 'template_name', 'personal_info_name', 
                  'photo', 'is_primary', 'has_complete_info', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_personal_info_name(self, obj):
        """Получение имени из личной информации"""
        if hasattr(obj, 'personal_info'):
            return obj.personal_info.full_name
        return None
    
    def get_has_complete_info(self, obj):
        """Проверка наличия основной информации"""
        return (
            hasattr(obj, 'personal_info') and
            obj.education.exists() and
            obj.work_experience.exists()
        )


class ResumeDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о резюме со всеми связанными данными"""
    personal_info = PersonalInfoSerializer(read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    work_experience = WorkExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_id = serializers.IntegerField(source='template.id', read_only=True)
    
    # Статистика
    sections_count = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = (
            'id', 'title', 'template', 'template_id', 'template_name', 'photo', 'is_primary',
            'personal_info', 'education', 'work_experience', 'skills', 
            'achievements', 'languages',
            'sections_count', 'completion_percentage',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_sections_count(self, obj):
        """Подсчет заполненных секций"""
        count = 0
        if hasattr(obj, 'personal_info'):
            count += 1
        if obj.education.exists():
            count += 1
        if obj.work_experience.exists():
            count += 1
        if obj.skills.exists():
            count += 1
        if obj.achievements.exists():
            count += 1
        if obj.languages.exists():
            count += 1
        return count
    
    def get_completion_percentage(self, obj):
        """Процент заполнения резюме"""
        total_sections = 6
        filled_sections = self.get_sections_count(obj)
        return round((filled_sections / total_sections) * 100)


class ResumeCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление резюме"""
    
    class Meta:
        model = Resume
        fields = ('title', 'template', 'photo', 'is_primary')

    def validate_title(self, value):
        """Валидация названия резюме"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Название резюме должно содержать минимум 3 символа")
        return value.strip()

    def validate_is_primary(self, value):
        """Обработка установки основного резюме"""
        if value:
            user = self.context['request'].user
            # Если устанавливаем резюме как основное, снимаем флаг с других
            if self.instance:
                # Обновление существующего резюме
                Resume.objects.filter(user=user, is_primary=True).exclude(pk=self.instance.pk).update(is_primary=False)
            else:
                # Создание нового резюме
                Resume.objects.filter(user=user, is_primary=True).update(is_primary=False)
        return value

    def create(self, validated_data):
        """Создание нового резюме"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Обновление существующего резюме"""
        # Если меняется шаблон, это может повлиять на отображение
        if 'template' in validated_data and validated_data['template'] != instance.template:
            # Можно добавить дополнительную логику при смене шаблона
            pass
        
        return super().update(instance, validated_data)