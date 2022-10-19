from unicodedata import name
from django.urls import path

from . import views
# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("wiki/<str:title>",views.show_entry, name="show_entry"),
    path("add_entry/",views.add_entry, name="add_entry"),
    path("edit_entry/<str:title>",views.edit_entry, name="edit_entry"),
    path("random_entry/",views.random_entry, name="random_entry"),
]
