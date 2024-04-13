from django.contrib.auth import get_user_model

from rest_framework import generics, request
from rest_framework import response, status
from rest_framework import decorators

from . import serializers, helpers

Users = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    queryset = Users.objects
    permission_classes = []


@decorators.api_view(["POST", ])
def activate_account(req: request.Request, user_id: int):
    query = Users.objects.filter(id=user_id)

    if not query.exists():
        return response.Response(
            {"Error": "This user_id has no related account"},
            status=status.HTTP_404_NOT_FOUND
            )

    helpers.activate_user(query.first())

    return response.Response({"Message": "User activated successfully"}, status=status.HTTP_200_OK)
