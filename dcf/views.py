# -*- coding:utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from dcf.models import Item, Image, Group, Section, FavoritsInfo
from dcf.forms import ItemCreateEditForm, ProfileForm, SearchForm


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
    paginate_by = settings.DCF_ITEM_PER_PAGE

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

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        obj = self.get_object()
        if not user.is_anonymous() and obj in user.favorites.all():
           context['like'] = 'mark'
        else:
           context['like'] = 'unmark'
        return context


class ItemUpdateView(FormsetMixin, UpdateView):
    is_update_view = True
    model = Item
    form_class = ItemCreateEditForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

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
    form_class = ItemCreateEditForm
    formset_class = inlineformset_factory(Item, Image, extra=3, fields=('file', ))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.allow_add_item():
            messages.error(self.request, _('You have reached the limit!'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyItemsView, self).dispatch(*args, **kwargs)


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('my')

    def get_object(self, queryset=None):
        obj = super(ItemDeleteView, self).get_object()
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemDeleteView, self).dispatch(*args, **kwargs)


class MyFavoritesItemsView(ListView):
    template_name = 'dcf/user_favorites_list.html'

    def get_queryset(self):
        Customer= self.request.user
        return Customer.favorites.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyFavoritesItemsView, self).dispatch(*args, **kwargs)


class FavItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('my')

    def get_object(self, queryset=None):
        obj = super(FavItemDeleteView, self).get_object()
        if not obj.user == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        user.favorites.remove(obj)
        return HttpResponseRedirect(reverse_lazy('my'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FavItemDeleteView, self).dispatch(*args, **kwargs)


class ProfileView(UpdateView):
    template_name = 'dcf/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        initial = super(ProfileView, self).get_initial()
        return initial

    def form_valid(self, form):
        messages.success(self.request, _('Your profile settings was updated!'))
        return super(ProfileView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'


def page403(request):
    return render(request, '403.html', {}, status=403)


def page404(request):
    return render(request, '404.html', {}, status=404)


def page500(request):
    return render(request, '500.html', {}, status=500)


@csrf_exempt
@login_required
def add_favorites(request):
    item_id = request.POST.get('item')
    user = request.user
    if request.is_ajax():
        user.favorites.add(item_id)
        FavoritsInfo.objects.create(
            customuser = user,
            item = Item.objects.get(pk=item_id)
        )
        message = "success"
    else:
        message = "error"
    return JsonResponse({'msg': message})


@csrf_exempt
@login_required
def del_favorites(request):
    item_id = request.POST.get('item')
    user = request.user
    if request.is_ajax():
        user.favorites.remove(item_id)
        FavoritsInfo.objects.filter(
            customuser = user,
            item = Item.objects.get(pk=item_id)
        ).delete()
        message = 'success'
    else:
        message = "error"
    return JsonResponse({'msg': message})