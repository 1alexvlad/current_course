from django.urls import path
from .views import CurrentView

app_name = 'currency'


urlpatterns = [
    path("get-current-usd/", CurrentView.as_view()),
]
