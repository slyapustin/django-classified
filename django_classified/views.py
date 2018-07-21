# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from . import settings as dcf_settings
from .forms import ItemForm, ProfileForm, SearchForm
from .models import Item, Image, Group, Section, Profile, Area


class FilteredListView(FormMixin, ListView):
    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            self.object_list = self.object_list.filter(**form.filter_by())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class SectionListView(TemplateView):
    template_name = 'django_classified/section_list.html'

    def get_context_data(self, **kwargs):
        context = super(SectionListView, self).get_context_data(**kwargs)

        items_qs = Item.active
        area = Area.get_for_request(self.request)
        if area:
            items_qs = items_qs.filter(area=area)

        object_list = []
        # Prepare list of tuples with object/count
        for section in Section.objects.all():
            groups = [(group, items_qs.filter(group=group).count()) for group in section.group_set.all()]
            object_list.append(dict(
                section=(section, items_qs.filter(group__section=section).count()),
                groups=groups
            ))

        context['object_list'] = object_list

        return context


class SearchView(FilteredListView):
    form_class = SearchForm
    queryset = Item.active.all()
    paginate_by = 10
    template_name = 'django_classified/search.html'

    def get_initial(self):
        initials = super(SearchView, self).get_initial()
        initials['area'] = Area.get_for_request(self.request)
        return initials


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        if hasattr(self, 'get_success_message'):
            self.get_success_message(form)
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class GroupDetail(SingleObjectMixin, ListView):
    paginate_by = dcf_settings.ITEM_PER_PAGE

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Group.objects.all())
        return super(GroupDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        context['group'] = self.object
        return context

    def get_queryset(self, **kwargs):
        item_qs = self.object.item_set.filter(is_active=True)
        area = Area.get_for_request(self.request)
        if area:
            return item_qs.filter(area=area)
        return item_qs


class ItemDetailView(DetailView):
    queryset = Item.active


class ItemUpdateView(FormsetMixin, UpdateView):
    is_update_view = True
    model = Item
    form_class = ItemForm
    formset_class = inlineformset_factory(Item, Image, fields=('file',))

    def get_object(self, *args, **kwargs):
        obj = super(ItemUpdateView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemUpdateView, self).dispatch(*args, **kwargs)


class ItemCreateView(FormsetMixin, CreateView):
    is_update_view = False
    model = Item
    form_class = ItemForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        profile = Profile.get_or_create_for_user(self.request.user)
        if not profile.allow_add_item():
            messages.error(self.request, _('You have reached the limit!'))
            return redirect(reverse('django_classified:user-items'))

        return super(ItemCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form, formset):
        form.instance.user = self.request.user
        form.save()

        return super(ItemCreateView, self).form_valid(form, formset)

    def get_initial(self):
        initial = super(ItemCreateView, self).get_initial()
        initial['area'] = Area.get_for_request(self.request)
        return initial


class MyItemsView(ListView):
    template_name = 'django_classified/user_item_list.html'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyItemsView, self).dispatch(*args, **kwargs)


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('django_classified:user-items')

    def get_queryset(self):
        qs = super(ItemDeleteView, self).get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)

        return qs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemDeleteView, self).dispatch(*args, **kwargs)


class ProfileView(UpdateView):
    template_name = 'django_classified/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('django_classified:profile')

    def get_object(self, queryset=None):
        return Profile.get_or_create_for_user(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your profile settings was updated!'))
        return super(ProfileView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)


class RobotsView(TemplateView):
    template_name = 'django_classified/robots.txt'
    content_type = 'text/plain'


class SetAreaView(View):
    def get(self, request):
        area_slug = request.GET.get('area_slug')
        if area_slug:
            area = get_object_or_404(Area, slug=area_slug)
            area.set_for_request(request)
        else:
            Area.delete_for_request(request)

        next_url = self.request.GET.get('next') or reverse_lazy('django_classified:index')

        return redirect(next_url)
