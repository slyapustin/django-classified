from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from dcf.models import Group, Section, Item

from dcf.api.serializers import GroupSerializer, SectionSerializer, ItemSerializer
from dcf.api.permissions import IsStaffOrReadOnly
from dcf.api.filters import ItemFilter


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsStaffOrReadOnly,)

    @detail_route(methods=['get', 'post'])
    def items(self, request, pk):
        items = Item.objects.filter(group=pk)

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsStaffOrReadOnly,)

    @detail_route(methods=['get', ])
    def groups(self, request, pk):
        groups = Group.objects.filter(section=pk)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    @detail_route(methods=['put'])
    def update_item(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            # TODO: return error code
            pass

    @detail_route(methods=['delete'])
    def delete(self, request, pk):
        item = self.queryset.get(pk=pk)
        item.delete()

        return Response()


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ItemFilter
