from rest_framework import serializers
from .models import Contributors


class ContributorSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    bio = serializers.CharField()
    contributor_id = serializers.IntegerField()

    def create(self, validated_data):
        return Contributors.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.bio=validated_data.get('bio',instance.bio)
        instance.contributor_id=validated_data.get('contributor_id',instance.contributor_id)
        instance.save()
        return instance
