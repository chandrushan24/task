from django.urls import path
from . import views

urlpatterns = [
    path('signal-sync/', views.signal_sync_view),
    path('signal-thread/', views.signal_thread_view),
    path('signal-transaction/', views.signal_transaction_view),
    path('rectangle/', views.rectangle_view),
]