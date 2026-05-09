from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Questionnaire
from .serializers import QuestionnaireSerializer


class QuestionnaireView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs, _ = Questionnaire.objects.get_or_create(user=request.user)
        return Response(QuestionnaireSerializer(qs).data)

    def patch(self, request):
        qs, _ = Questionnaire.objects.get_or_create(user=request.user)
        serializer = QuestionnaireSerializer(qs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

