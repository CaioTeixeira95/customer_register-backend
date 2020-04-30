from ..models import Customer
from .serializers import CustomerSerializer, UserRegisterSerializer
from djangorestframework_camel_case.parser import CamelCaseJSONParser, CamelCaseFormParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User


class CustomObtainToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': f'{user.first_name} {user.last_name}'
        })


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    parser_classes = [CamelCaseJSONParser, CamelCaseFormParser]
    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.prefetch_related('addresses_set').filter(
            user=user
        ).order_by('name')

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            user=user
        )


class UserRegisterCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    parser_classes = [CamelCaseJSONParser, CamelCaseFormParser]
    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
    permission_classes = (AllowAny,)
