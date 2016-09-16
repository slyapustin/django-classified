from django.core.exceptions import ObjectDoesNotExist

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

    def create(self, request):
        if not request.user.is_staff:
            return Response(status=403)
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()

    # TODO: return error code if object not valid

    def update(self, request, pk):
        print(request.user)
        if not request.user.is_staff:
            return Response(status=403)
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
        if not request.user.is_staff:
            return Response(status=403)
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
        if not request.user.is_staff:
            return Response(status=403)
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()

    def update(self, request, pk):
        if not request.user.is_staff:
            return Response(status=403)
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
        if not request.user.is_staff:
            return Response(status=403)
        try:
            item = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        item.delete()

        return Response()


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ItemFilter

    def create(self, request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return Response(status=403)
        print(request.user)
        request.data['user'] = request.user.id
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()

    def update(self, request, pk):
        try:
            item = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        if not item.user == request.user:
            return Response(status=403)
        serialzer = self.serializer_class(item, request.data)
        if serialzer.is_valid():
            serialzer.save()
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
