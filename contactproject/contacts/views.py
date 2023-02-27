from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from core.functions import is_ajax
from core.mixins import PaginationMixin, ModelMixin, SuccessUrlMixin,FormMixin,QueryListMixin, AjaxDeleteMixin


from .models import Contact, Telephone,Address, Email
from .forms import ContactForm, AddressFormSet, TelephoneFormSet, EmailFormSet


class ContactListView(PaginationMixin,QueryListMixin,ModelMixin, LoginRequiredMixin, ListView):
    model = Contact
    queryset = Contact.objects.select_related('profile').prefetch_related('addresses', 'phones', 'emails')
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_list_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class ContactCreateView(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Contact
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Address',
                'formset': AddressFormSet(self.request.POST or None)
            },
            {
                'title': 'Telephone',
                'formset': TelephoneFormSet(self.request.POST or None)
            },
            {
                'title': 'Email',
                'formset': EmailFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = self.request.user.profile
            obj.save()
            formsets = [
                AddressFormSet(self.request.POST, instance=obj),
                TelephoneFormSet(self.request.POST, instance=obj),
                EmailFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class ContactUpdateView(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Contact
    form_class = ContactForm

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Address',
                'formset': AddressFormSet(
                    self.request.POST or None,instance=self.get_object()),
            },
            {
                'title': 'Telephone',
                'formset': TelephoneFormSet(
                    self.request.POST or None,instance=self.get_object()),
            },
            {
                'title': 'Email',
                'formset': EmailFormSet(
                    self.request.POST or None,instance=self.get_object()),
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            formsets = [
                AddressFormSet(self.request.POST, instance=obj),
                TelephoneFormSet(self.request.POST, instance=obj),
                EmailFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)

class ContactDeleteView(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Contact
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

