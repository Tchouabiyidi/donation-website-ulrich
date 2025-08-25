from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)  # Create token on user creation
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Ensure role for superuser
        extra_fields.setdefault('role', CustomUser.Role.SUPERADMIN)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    accept_terms = models.BooleanField(_('terms accepted'), default=False)
    newsletter = models.BooleanField(_('newsletter subscribed'), default=False)
    
    class Gender(models.TextChoices):
        FEMALE = 'female', _('Female')
        MALE = 'male', _('Male')
    
    class Role(models.TextChoices):
        DONOR = 'donor', _('Donor')
        CAMPAIGN_MANAGER = 'campaign_manager', _('Campaign Manager')
        SUPERADMIN = 'superadmin', _('Super Admin')

    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.DONOR,
    )
    gender = models.CharField(_('gender'), max_length=10, choices=Gender.choices, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Profile models for role-specific data
class DonorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DonorProfile<{self.user_id}>"


class CampaignOrganizerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer_profile')
    charity_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def verify(self):
        self.verified = True
        self.save(update_fields=['verified'])

    def __str__(self):
        return f"OrganizerProfile<{self.user_id}>"


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AdminProfile<{self.user_id}>"


class Campaign(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    # Must be true before being displayed to donors
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def end_campaign(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def __str__(self):
        return f"Campaign<{self.pk}:{self.title}>"


class Payment(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def process_donation(self):
        self.status = 'succeeded'
        self.save(update_fields=['status'])

    def __str__(self):
        return f"Payment<{self.pk}> {self.amount} by {self.donor_id}"


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_notification(self):
        # Placeholder for sending notification
        return True

    def __str__(self):
        return f"Notification<{self.pk}>"