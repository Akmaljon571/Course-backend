from django.urls import path

from .views import RegionOneView, RegionAllView

urlpatterns = [
    path('<int:pk>', RegionOneView.as_view()),
    path('', RegionAllView.as_view())
]
