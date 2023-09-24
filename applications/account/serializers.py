# from django.contrib.auth import get_user_model
# from rest_framework import serializers
from applications.account.task import send_confirmation_email

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['email', 'password', 'password_confirm']

#     def validate(self, attrs):
#         p1 = attrs.get('password')
#         p2 = attrs.pop('password_confirm')

#         if p1 != p2:
#             raise serializers.ValidationError("Password isn't same")
#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         code = user.activation_code
#         send_confirmation_email(user.email, code)
#         return user

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password_confirm', 'first_name', 'last_name']  # Добавьте остальные необходимые поля

        # Если вы хотите, чтобы все поля были обязательными, вы можете также установить опцию extra_kwargs
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError("Password isn't same")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.create_activation_code()  # Вызываем метод для создания activation_code
        user.save()
        code = user.activation_code
        send_confirmation_email(user.email, code)
        return user
