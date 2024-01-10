from rest_framework import serializers

from .models import CustomUser


class RegistrationCodeSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('code',)


class PasswordCodeSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()
    new_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('code', 'new_password')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class RegistrationSchemaCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6)

    class Meta:
        model = CustomUser
        fields = ('username', 'age', 'region', 'phone', 'avatar', 'code')
        extra_kwargs = {'password': {'write_only': True}, 'avatar': {'required': False}}


class RegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'age', 'region', 'phone', 'avatar', 'password', 'email')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PasswordEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'region', 'phone', 'avatar', 'discount')

