from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from django.db import models

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
            self.object_list = self.object_list.filter(form.get_queryset_filter())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class SectionListView(TemplateView):
    template_name = 'django_classified/section_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        area = Area.get_for_request(self.request)

        item_filter = models.Q(item__is_active=True)
        if area:
            item_filter &= models.Q(item__area=area)

        groups = (
            Group.objects
            .select_related('section')
            .annotate(item_count=models.Count('item', filter=item_filter))
            .order_by('section__title', 'title')
        )

        sections_dict = {
            section.pk: {'section': (section, 0), 'groups': []}
            for section in Section.objects.all()
        }
        for group in groups:
            section = group.section
            if section.pk not in sections_dict:
                sections_dict[section.pk] = {'section': (section, 0), 'groups': []}
            sections_dict[section.pk]['groups'].append((group, group.item_count))
            sections_dict[section.pk]['section'] = (
                section,
                sections_dict[section.pk]['section'][1] + group.item_count,
            )

        context['object_list'] = list(sections_dict.values())

        return context


class SearchView(FilteredListView):
    form_class = SearchForm
    queryset = Item.active.prefetch_related('image_set')
    paginate_by = 10
    template_name = 'django_classified/search.html'

    def get_initial(self):
        initials = super().get_initial()
        initials['area'] = Area.get_for_request(self.request)
        return initials


class FormsetMixin:
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
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        return context

    def get_queryset(self, **kwargs):
        item_qs = (
            self.object.item_set
            .filter(is_active=True)
            .prefetch_related('image_set')
        )
        area = Area.get_for_request(self.request)
        if area:
            return item_qs.filter(area=area)
        return item_qs


class ItemDetailView(DetailView):
    queryset = Item.active.select_related('group__section', 'area', 'user__profile').prefetch_related('image_set')


class ItemUpdateView(LoginRequiredMixin, FormsetMixin, UpdateView):
    is_update_view = True
    model = Item
    form_class = ItemForm
    formset_class = inlineformset_factory(Item, Image, fields=('file',))

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class ItemCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    is_update_view = False
    model = Item
    form_class = ItemForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        profile = Profile.get_or_create_for_user(request.user)
        if not profile.allow_add_item():
            messages.error(request, _('You have reached the limit!'))
            return redirect(reverse('django_classified:user-items'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form, formset):
        form.instance.user = self.request.user
        form.save()

        return super().form_valid(form, formset)

    def get_initial(self):
        initial = super().get_initial()
        initial['area'] = Area.get_for_request(self.request)
        return initial


class MyItemsView(LoginRequiredMixin, ListView):
    template_name = 'django_classified/user_item_list.html'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).select_related('group__section')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('django_classified:user-items')

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)

        return qs


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'django_classified/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('django_classified:profile')

    def get_object(self, queryset=None):
        return Profile.get_or_create_for_user(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your profile settings was updated!'))
        return super().form_valid(form)


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

        next_url = self.request.GET.get('next', '')
        if not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            next_url = reverse('django_classified:index')

        return redirect(next_url)
