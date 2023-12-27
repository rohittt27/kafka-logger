from django.urls import path
from api.views import ItemList, ItemDetail

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail')
    # path('login/', UserLoginView.as_view(), name='login')
]