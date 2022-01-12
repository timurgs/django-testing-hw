from rest_framework import serializers

from students.models import Course
from django_testing import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if len(data.get('students')) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('The number of students per course should not exceed 20')
        return data
