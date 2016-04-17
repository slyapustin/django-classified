from rest_framework import viewsets

from dcf.models import Group, Section
from dcf.api.serializers import GroupSerializer, SectionSerializer
from dcf.api.permissions import IsStaffOrReadOnly


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsStaffOrReadOnly,)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsStaffOrReadOnly,)
