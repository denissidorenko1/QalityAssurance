from rest_framework import serializers
from .models import Contributors, Tables


class ContributorSerializer(serializers.Serializer):
    #зачем объявлять?
    title = serializers.CharField(max_length=120)
    bio = serializers.CharField()
    contributor_id = serializers.IntegerField()

    def create(self, validated_data):
        return Contributors.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.bio=validated_data.get('bio',instance.bio)
        instance.contributor_id=validated_data.get('contributor_id',instance.contributor_id) # needs to be removed
        instance.save()
        return instance


class EquipmentSerializer(serializers.Serializer):
    equip = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    approved_by_manager = serializers.BooleanField(default=0)
    delivered = serializers.BooleanField(default=0)

    def create(self, validated_data):
        return Tables.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.equip=validated_data.get('equip',instance.equip)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.approved_by_manager = validated_data.get('approved_by_manager', instance.approved_by_manager)
        instance.delivered = validated_data.get('delivered', instance.delivered)
        instance.save()
        return instance
