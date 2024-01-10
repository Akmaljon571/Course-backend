from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from user.permissions import IsUserReadAndWriteAdmin
from .serializers import RegionSerializer
from .models import RegionModel


class RegionAllView(ListCreateAPIView):
    queryset = RegionModel.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsUserReadAndWriteAdmin,)


class RegionOneView(RetrieveUpdateDestroyAPIView):
    queryset = RegionModel.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsUserReadAndWriteAdmin,)
