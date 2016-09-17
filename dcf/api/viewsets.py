from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        # TODO: return error code if object not valid

    def update(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        serializer = self.serializer_class(group, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        # TODO: return error code if object not valid

    def destroy(self, request, pk):
        try:
            group = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        group.delete()

        return Response()


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsStaffOrReadOnly,)

    @detail_route(methods=['get', ])
    def groups(self, request, pk):
        groups = Group.objects.filter(section=pk)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()

    def update(self, request, pk):
        try:
            section = Section.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        serializer = self.serializer_class(section, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        # TODO: return error code if object not valid

    def destroy(self, request, pk):
        try:
            item = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        item.delete()

        return Response()


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ItemFilter

    def create(self, request):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        # TODO: return error

    def update(self, request, pk):
        try:
            item = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        if not item.user == request.user:
            return Response(status=403)
        request.data['user'] = request.user.id
        serializer = self.serializer_class(item, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        # TODO: return error code if object not valid

    def destroy(self, request, pk):
        try:
            item = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        if not item.user == request.user:
            return Response(status=403)
        item.delete()

        return Response()
