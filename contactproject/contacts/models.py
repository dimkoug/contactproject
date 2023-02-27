from django.db import models

# Create your models here.
from profiles.models import Profile
from core.models import Timestamped


class Contact(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    class Meta:
        default_related_name = 'contacts'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return f"{self.surname}, {self.first_name}"


class Address(Timestamped):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    class Meta:
        default_related_name = 'addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.address}"


class Telephone(Timestamped):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)

    class Meta:
        default_related_name = 'phones'
        verbose_name = 'phone'
        verbose_name_plural = 'phones'

    def __str__(self):
        return f"{self.phone}"


class Email(Timestamped):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        default_related_name = 'emails'
        verbose_name = 'email'
        verbose_name_plural = 'emails'

    def __str__(self):
        return f"{self.email}"

