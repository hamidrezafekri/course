from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from socialmedia.api.mixins import ApiAuthMixin
from socialmedia.api.pagination import LimitOffsetPagination, get_paginated_response
from socialmedia.blog.models import Subcription
from socialmedia.blog.selectors.posts import get_subscribers
from socialmedia.blog.services.post import unsubscribe, subscribe


class SubscribeDetailApi(ApiAuthMixin , APIView):

    def delete(self , request , email):

        try:
            unsubscribe(user= request.user , email = email)
        except Exception as ex:
            return Response(
                {"detail": "database error" + str(ex)},
                status= status.HTTP_400_BAD_REQUEST
            )
        return Response(status = status.HTTP_204_NO_CONTENT)


class SubscribeApi(ApiAuthMixin , APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)


    class OutPutSubSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField('get_username')

        class Meta:
            model = Subcription
            fields = ("email" ,)

        def get_username(self , subscription):
            return subscription.target.email

    @extend_schema(
        responses=OutPutSubSerializer,
    )
    def get(self , request):
        user = request.user
        query = get_subscribers(user = user)
        return get_paginated_response(
            request = request,
            pagination_class = self.Pagination,
            queryset = query,
            serializer_class = self.OutPutSubSerializer,
            view = self,
        )

    @extend_schema(
        request=InputSubSerializer,
        responses=OutPutSubSerializer,
    )
    def post(self , request):
        serializer = self.InputSubSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = subscribe(user = request.user , email = serializer.validated_data.get("email"))
        except Exception as ex:
            return Response(
                {"detail" :"DATABASE Error" + str(ex)},
                status = status.HTTP_400_BAD_REQUEST,
            )
        output_serializer = self.OutPutSubSerializer(query)
        return Response(output_serializer.data)
