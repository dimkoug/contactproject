from django import forms
from django.forms import inlineformset_factory
from django.forms import BaseFormSet, formset_factory
from core.forms import BootstrapForm, BootstrapFormSet

from .models import Contact, Address, Telephone, Email

class ContactForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'surname')


class AddressForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address',)


class TelephoneForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Telephone
        fields = ('phone',)
    

class EmailForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Email
        fields = ('email',)




AddressFormSet = inlineformset_factory(Contact, Address, form=AddressForm, formset=BootstrapFormSet, extra=1, can_delete=True, can_delete_extra=True)
TelephoneFormSet = inlineformset_factory(Contact, Telephone, form=TelephoneForm,formset=BootstrapFormSet, extra=1, can_delete=True, can_delete_extra=True)
EmailFormSet = inlineformset_factory(Contact, Email, form=EmailForm,formset=BootstrapFormSet, extra=1, can_delete=True, can_delete_extra=True)