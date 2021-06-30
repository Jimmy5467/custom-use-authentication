from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User, UserManager
from allauth.account.utils import setup_user_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, write_only=True, )
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    # address = serializers.CharField(required=False, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    city = serializers.CharField(required=True, write_only=True)
    license = serializers.CharField(required=True, write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'city': self.validated_data.get('city', ''),
            'license': self.validated_data.get('license', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
        # adapter = get_adapter()
        # user = adapter.new_user(request)
        # user = adapter.save_user(request, user, self, commit=False)
        # user.preferred_locale = self.validated_data.get('preferred_locale', 'en')
        # user.save()
        # self.custom_signup(request, user)
        # setup_user_email(request, user, [])
        #return user

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'phone', 'first_name', 'last_name', 'city', 'license')
        read_only_fields = ('email',)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
