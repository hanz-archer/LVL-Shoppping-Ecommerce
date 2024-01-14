from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.dashboard_products, name="dashboard-products"),
    path("add-products/", views.dashboard_add_product, name="dashboard-add-products"),
    path("edit-products/<pid>/", views.dashboard_edit_product, name="dashboard-edit-products"),
    path("delete-products/<pid>/", views.dashboard_delete_product, name="dashboard-delete-products"),
]
