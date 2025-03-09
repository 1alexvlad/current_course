from django.urls import path
from .views import CurrentView
from django.views.decorators.cache import cache_page


app_name = 'currency'


urlpatterns = [
    path("get-current-usd/", cache_page(10)(CurrentView.as_view())),
]
