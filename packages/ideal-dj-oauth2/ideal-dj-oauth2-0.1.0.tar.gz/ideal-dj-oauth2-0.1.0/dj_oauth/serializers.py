from rest_framework import serializers
from .models import User, Role, Scope, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'date_of_birth', 'first_name', 'last_name')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'scopes')

class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ('id', 'name', 'description')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'members')
