from rest_framework import generics

from apps.rubric.models import Rubric
from apps.rubric.serializers import RubricListSerializer, RubricDetailSerializer


class RubricList(generics.ListCreateAPIView):

    queryset = Rubric.objects.all()
    serializer_class = RubricListSerializer


class RubricDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Rubric.objects.all()
    serializer_class = RubricDetailSerializer


class RubricChildrenOfList(generics.ListCreateAPIView):

    serializer_class = RubricListSerializer

    def get_queryset(self):
        return Rubric.objects.get(pk=self.kwargs['pk']).get_children()