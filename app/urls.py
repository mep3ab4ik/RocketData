from django.urls import path, include
from app.api import view


urlpatterns = [
    path('create_company/', view.CreateCompanyView.as_view()),
    path('company/product/<int:pk>', view.FindCompanyWithProductView.as_view()),
    path('remove_company/<int:pk>/', view.RemoveCompanyView.as_view()),
    path('update_company/<int:pk>', view.UpdateCompanyView.as_view()),
    path('company/<str:country>/', view.CountyCompanyView.as_view()),
    path('company/', view.CompanyView.as_view()),
    path('create_product/', view.CreateProductsView.as_view()),
    path('update_product/<int:pk>', view.UpdateProductView.as_view()),
    path('remove_product/<int:pk>/', view.RemoveProductsView.as_view()),
    path('statistics/', view.MoreAvgDebtView.as_view()),
]