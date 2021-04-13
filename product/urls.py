from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'product-home'),
    path('add/',views.create_product, name = 'product-add'),
    path('edit/',views.edit_product, name = 'product-edit'),
    path('<int:p_id>/', views.edit_util, name='product_edit_util'),
    path('view/',views.view_product, name = 'product-view'),
    path('transaction/', views.new_transaction, name='product-transaction'),
    path('pay/', views.generate_pdf, name='product-pay'),
    path('clear/', views.clear, name='product-clear'),
    path('complete/', views.complete_transaction, name='product-complete'),
    path('report/',views.report, name='product-report'),
    path('report/user/<int:u_id>', views.user_report, name='product-user-report'),

    path('chart/', views.chart_home, name='product-chart-home'),
    path('chart/api/', views.create_chart),
]

