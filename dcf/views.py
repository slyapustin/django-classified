# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from dcf import settings as dcf_settings
from dcf.forms import ItemForm, ProfileForm, SearchForm
from dcf.models import Item, Image, Group, Section, Profile


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


class SectionListView(ListView):
    model = Section


class SearchView(FilteredListView):
    form_class = SearchForm
    queryset = Item.objects.filter(is_active=True)
    paginate_by = 10
    template_name = 'dcf/search.html'


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
    paginate_by = dcf_settings.DCF_ITEM_PER_PAGE

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Group.objects.all())
        return super(GroupDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        context['group'] = self.object
        return context

    def get_queryset(self):
        return self.object.item_set.all()


class ItemDetailView(DetailView):
    queryset = Item.objects.filter(is_active=True)


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
            return redirect(reverse('dcf:user-items'))

        return super(ItemCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form, formset):
        form.instance.user = self.request.user
        form.save()

        return super(ItemCreateView, self).form_valid(form, formset)


class MyItemsView(ListView):
    template_name = 'dcf/user_item_list.html'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyItemsView, self).dispatch(*args, **kwargs)


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('dcf:user-items')

    def get_queryset(self):
        qs = super(ItemDeleteView, self).get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)

        return qs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemDeleteView, self).dispatch(*args, **kwargs)


class ProfileView(UpdateView):
    template_name = 'dcf/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('dcf:profile')

    def get_object(self, queryset=None):
        return Profile.get_or_create_for_user(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your profile settings was updated!'))
        return super(ProfileView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)


class RobotsView(TemplateView):
    template_name = 'dcf/robots.txt'
    content_type = 'text/plain'
