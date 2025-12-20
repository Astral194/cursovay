# app/urls.py
from django.urls import path
from .views import (login_view, logout_view,
                    dashboard, add_employee, export_excel,
                    edit_row, delete_row, add_row)

urlpatterns = [
    path("", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path('add_employee/', add_employee, name='add_employee'),
    path('edit_row/<str:table>/<int:row_id>/', edit_row, name='edit_row'),
    path('delete_row/', delete_row, name='delete_row'),
    path('export_excel/', export_excel, name='export_excel'),
    path("add_row/<str:table>/", add_row, name="add_row"),
]
