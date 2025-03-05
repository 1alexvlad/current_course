import requests
from datetime import datetime

from .models import CurrencyModel

from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone



class CurrentView(View):
    def get(self, request):
        url = "http://apilayer.net/api/live?access_key=" + settings.API_KEY
        response = requests.get(url)
        data = response.json()

        value = data['quotes']['USDRUB']

        last_value = CurrencyModel.objects.all().order_by('-datetime')[:1]

        if last_value:
            last_datetime = last_value[0].datetime
            current_datetime = timezone.now() 

            time_diff = current_datetime - last_datetime

            if time_diff.total_seconds() > 10:
                CurrencyModel.objects.create(price=value)
        else:
            CurrencyModel.objects.create(price=value)

        history_last_10 = CurrencyModel.objects.all().order_by('-datetime')[:10]

        return JsonResponse({
            'Цена': value,
            'Последние 10 запросов': [{'datetime': req.datetime.strftime('%Y-%m-%d %H:%M:%S'), 'price': req.price} for req in history_last_10]
        })
