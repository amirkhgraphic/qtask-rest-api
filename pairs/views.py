from rest_framework import generics

from .models import KeyValue
from .serializers import KeyValueSerializer
from .filters import KeyValueFilter


class KeyValueListCreateAPIView(generics.ListCreateAPIView):
    queryset = KeyValue.objects.filter(parent__isnull=True)
    serializer_class = KeyValueSerializer


class KeyValueRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer


class KeyValueFilterListAPIView(generics.ListAPIView):
    queryset = KeyValue.objects.filter()
    serializer_class = KeyValueSerializer
    filterset_class = KeyValueFilter
    search_fields = ['key']
