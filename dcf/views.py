# -*- coding:utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView,  UpdateView, ListView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from .models import Item, Image, Group, Section
from .forms import ItemCreateEditForm, ProfileForm, SearchForm


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


def index(request):

    return render(request, 'dcf/index.html', {
        'groups': Group.objects.all(),
        'sections': Section.objects.all()
    })


class SearchView(FilteredListView):

    form_class = SearchForm
    queryset = Item.objects.filter(is_active=True).all()
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

    paginate_by = 10
    template_name = 'dcf/group_detail.html'

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

    template_name = 'dcf/item_form.html'
    is_update_view = True
    model = Item
    form_class = ItemCreateEditForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

    def get_object(self, *args, **kwargs):
        obj = super(ItemUpdateView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class ItemCreateView(FormsetMixin, CreateView):

    template_name = 'dcf/item_form.html'
    is_update_view = False
    model = Item
    form_class = ItemCreateEditForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.allow_add_item():
            messages.error(self.request, 'You have reached limit!')
            return redirect(reverse('my'))

        return super(ItemCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form, formset):

        form.instance.user = self.request.user
        form.save()

        return super(ItemCreateView, self).form_valid(form, formset)


class MyItemsView(ListView):

    template_name = 'dcf/user_item_list.html'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDeleteView(DeleteView):

    model = Item
    success_url = reverse_lazy('my')

    def get_object(self, queryset=None):
        obj = super(ItemDeleteView, self).get_object()
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


@login_required
def view_profile(request):

    if request.method == 'GET':
        form = ProfileForm(instance=request.user, initial={'email': request.user.email})
    else:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():

            form.save()
            messages.success(request, u'Your profile settings was updated!')

            return redirect(reverse('profile'))

    return render(request, 'dcf/profile.html', {'form': form})


def robots(request):
    return render(request, 'robots.txt', {'domain': Site.objects.get_current().domain}, content_type='text/plain')


def page403(request):
    return render(request, '403.html', {}, status=403)


def page404(request):
    return render(request, '404.html', {}, status=404)


def page500(request):
    return render(request, '500.html', {}, status=500)