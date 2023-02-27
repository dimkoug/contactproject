from django.urls import path

from .views import (
    ContactListView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
)


app_name = 'contacts'


urlpatterns = [
    path('',ContactListView.as_view(),name='contact-list'),
    path('create/',ContactCreateView.as_view(),name='contact-create'),
    path('update/<int:pk>/',ContactUpdateView.as_view(),name='contact-update'),
    path('delete/<int:pk>/',ContactDeleteView.as_view(),name='contact-delete'),
]