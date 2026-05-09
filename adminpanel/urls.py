from django.urls import path

from .views import (
    AllUserView,
    UserView,
    EditUserView,
    AllProductsView,
    SingleProductView,
    AddProductView,
    EditProductView,
    soft_delete_view,
    AllOrdersView,
    UpdateOrderStatusView,
    DashboardRevenueView
)

urlpatterns = [

    path("users/", AllUserView.as_view()),
    path("users/<int:pk>/", UserView.as_view()),
    path("users/<int:pk>/edit/", EditUserView.as_view()),

    path("products/", AllProductsView.as_view()),
    path("products/<int:pk>/", SingleProductView.as_view()),
    path("products/add/", AddProductView.as_view()),
    path("products/<int:pk>/edit/", EditProductView.as_view()),
    path("products/<int:pk>/delete/", soft_delete_view),

    path("orders/", AllOrdersView.as_view()),
    path("orders/<int:pk>/update/", UpdateOrderStatusView.as_view()),

    path("dashboard/", DashboardRevenueView.as_view()),
]
# from django.urls import path
# from .views import (
#     AdminUserListView,
#     AdminProductListView,
#     AdminProductCreateView,
#     AdminProductUpdateView,
#     AdminProductDeleteView,
#     AdminOrderListView,
#     AdminOrderUpdateView,
# )

# urlpatterns = [
#     path("users/", AdminUserListView.as_view()),

#     path("products/", AdminProductListView.as_view()),
#     path("products/create/", AdminProductCreateView.as_view()),
#     path("products/<int:product_id>/update/", AdminProductUpdateView.as_view()),
#     path("products/<int:product_id>/delete/", AdminProductDeleteView.as_view()),

#     path("orders/", AdminOrderListView.as_view()),
#     path("orders/<int:order_id>/update/", AdminOrderUpdateView.as_view()),
# ]