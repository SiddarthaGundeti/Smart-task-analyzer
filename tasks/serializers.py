from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
id = serializers.IntegerField(required=False)
title = serializers.CharField()
due_date = serializers.DateField()
estimated_hours = serializers.IntegerField()
importance = serializers.IntegerField()
dependencies = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
