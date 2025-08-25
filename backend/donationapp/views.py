from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer, UserListSerializer, CampaignSerializer, NotificationSerializer
from .models import Campaign, Notification
from django.contrib.auth import login
from django.contrib.auth import get_user_model

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