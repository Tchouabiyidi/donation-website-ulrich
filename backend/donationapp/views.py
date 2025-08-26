from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer, UserListSerializer, CampaignSerializer, NotificationSerializer
from .models import Campaign, Notification
from django.contrib.auth import login
from django.contrib.auth import get_user_model
import os
import json
import logging

import requests

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': getattr(user, 'role', None),
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'errors': serializer.errors,
            'message': 'Registration failed'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.pk,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': getattr(user, 'role', None),
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                }
            }, status=status.HTTP_200_OK)
            
        return Response({
            'errors': serializer.errors,
            'message': 'Login failed'
        }, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': getattr(user, 'role', None),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Revoke the current token
        try:
            Token.objects.filter(user=request.user).delete()
        except Exception:
            pass
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Only superadmin or is_superuser can list users
        role = getattr(user, 'role', None)
        if not (getattr(user, 'is_superuser', False) or role == 'superadmin'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        User = get_user_model()
        qs = User.objects.all().order_by('id')
        data = UserListSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        role = getattr(user, 'role', None)
        if not (getattr(user, 'is_superuser', False) or role == 'superadmin'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        User = get_user_model()
        try:
            target = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if target.pk == user.pk:
            return Response({'detail': 'You cannot delete your own account.'}, status=status.HTTP_400_BAD_REQUEST)

        target.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)


class CampaignCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        role = getattr(user, 'role', None)
        if role != 'campaign_manager' and not getattr(user, 'is_superuser', False):
            return Response({'detail': 'Only campaign organizers can create campaigns.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.save(organizer=user)
            return Response(CampaignSerializer(campaign).data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'message': 'Campaign creation failed'}, status=status.HTTP_400_BAD_REQUEST)


class CampaignPendingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = getattr(user, 'role', None)
        if not (getattr(user, 'is_superuser', False) or role == 'superadmin'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        qs = Campaign.objects.filter(is_validated=False).order_by('-created_at')
        data = CampaignSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return notifications sent to this user (as recipient)
        qs = Notification.objects.filter(sender=request.user).order_by('-created_at')  # adjust if recipient exists later
        data = NotificationSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class NotificationReadToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk: int):
        try:
            n = Notification.objects.get(pk=pk, sender=request.user)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        # Toggle is_read or set from payload
        set_value = request.data.get('is_read')
        if isinstance(set_value, bool):
            n.is_read = set_value
        else:
            n.is_read = not n.is_read
        n.save(update_fields=['is_read'])
        return Response(NotificationSerializer(n).data, status=status.HTTP_200_OK)


class NotificationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk: int):
        try:
            n = Notification.objects.get(pk=pk, sender=request.user)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        n.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CampaignValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk: int):
        user = request.user
        role = getattr(user, 'role', None)
        if not (getattr(user, 'is_superuser', False) or role == 'superadmin'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response({'detail': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)

        if campaign.is_validated:
            return Response({'message': 'Campaign already validated'}, status=status.HTTP_200_OK)

        campaign.is_validated = True
        campaign.save(update_fields=['is_validated'])
        return Response(CampaignSerializer(campaign).data, status=status.HTTP_200_OK)


class CampaignApprovedListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Campaign.objects.filter(is_validated=True, is_active=True).order_by('-created_at')
        data = CampaignSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


# -----------------------------
# Campay Integration (minimal)
# -----------------------------

logger = logging.getLogger(__name__)

def _campay_config():
    base_url = os.getenv('CAMPAY_BASE_URL', '').rstrip('/')
    token = os.getenv('CAMPAY_ACCESS_TOKEN', '')
    currency = os.getenv('CAMPAY_CURRENCY', 'XAF')
    if not base_url or not token:
        return None
    return {
        'base_url': base_url,
        'token': token,
        'currency': currency,
    }


class CampayCollectView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cfg = _campay_config()
        if not cfg:
            return Response({'detail': 'Campay not configured. Missing CAMPAY_BASE_URL or CAMPAY_ACCESS_TOKEN.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        amount = request.data.get('amount')
        msisdn = request.data.get('msisdn') or request.data.get('phone')
        description = request.data.get('description', 'Donation')
        currency = request.data.get('currency', cfg['currency'])
        external_reference = request.data.get('reference')

        if not amount or not msisdn:
            return Response({'detail': 'amount and msisdn are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = {
                'amount': str(amount),
                'from': str(msisdn),
                'description': description,
                'currency': currency,
            }
            if external_reference:
                payload['external_reference'] = str(external_reference)

            headers = {
                'Authorization': f"Token {cfg['token']}",
                'Content-Type': 'application/json',
            }

            # Common Campay path for collection is '/collect/' (trailing slash avoids 301/302 redirect)
            url = f"{cfg['base_url'].rstrip('/')}/collect/"
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
            data = resp.json() if resp.content else {}
            return Response({'status_code': resp.status_code, 'provider_response': data}, status=resp.status_code if 200 <= resp.status_code < 300 else status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            logger.exception('Campay collect request failed')
            return Response({'detail': 'Campay request failed', 'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class CampayWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        # Note: Signature verification depends on Campay webhook config.
        # We accept and log the payload; add signature check if header/name provided.
        try:
            payload = request.data
            # Raw body for auditing
            try:
                raw_body = request.body.decode('utf-8')
            except Exception:
                raw_body = None

            # Optionally check signature header if present (e.g., 'X-Campay-Signature')
            signature = request.headers.get('X-Campay-Signature') or request.headers.get('X-CAMPAY-SIGNATURE')
            logger.info('Campay webhook received. Signature=%s Payload=%s Raw=%s', signature, payload, raw_body)

            # TODO: implement strict signature verification when header/algorithm is confirmed.

            # Respond 200 OK so Campay considers it delivered.
            return Response({'received': True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Campay webhook handling failed')
            return Response({'detail': 'Webhook processing error', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)