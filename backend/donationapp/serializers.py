from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Campaign, Notification
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 
                 'last_name', 'phone', 'accept_terms', 'newsletter', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'accept_terms': {'required': True},
        }
    

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
            
        # Restrict role assignment during self-registration to donor or campaign_manager only
        requested_role = data.get('role')
        allowed_roles = {'donor', 'campaign_manager'}
        if requested_role is None:
            data['role'] = getattr(User, 'Role').DONOR if hasattr(User, 'Role') else 'donor'
        elif requested_role not in allowed_roles:
            raise serializers.ValidationError({"role": "Role must be 'donor' or 'campaign_manager' for self-registration."})
        return data

    def create(self, validated_data):
        # Remove confirm_password, not a model field
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        # Use custom manager to hash password and create token
        user = User.objects.create_user(password=password, **validated_data)
        return user


class NotificationSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read', 'sender_email']
        read_only_fields = ['id', 'created_at', 'sender_email']

    def get_sender_email(self, obj):
        try:
            return getattr(obj.sender, 'email', None)
        except Exception:
            return None


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active']


class CampaignSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    is_validated = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id', 'organizer', 'title', 'description', 'target_amount',
            'start_date', 'end_date', 'is_active', 'is_validated',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'organizer', 'is_active', 'is_validated', 'created_at', 'updated_at']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = User.objects.filter(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        
        return data