from rest_framework import serializers
from .models import UserNet
from rest_framework.renderers import JSONRenderer

    



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNet
        fields = ("pk", "first_name", "last_name", "username")

# class UserSerializer(serializers.Serializer):
    
#     last_name = serializers.CharField(max_length=255)
#     first_name = serializers.CharField(max_length=255)
#     username = serializers.CharField(max_length=255)
#     date_joined = serializers.DateTimeField(read_only=True)
    
#     def create(self,validated_data):
#         return UserNet.objects.create(**validated_data)

#     def update (self,instance,validated_data):
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.username = validated_data.get('username', instance.username)
#         instance.save()
#         return instance
    




